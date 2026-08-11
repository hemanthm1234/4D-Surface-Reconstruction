import os
import fitz  # PyMuPDF
import re
import io
import base64
from PIL import Image
from openai import OpenAI
import time

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def is_architecture_diagram_openrouter(image, api_key):
    """
    Uses OpenRouter (OpenAI compatible API) to verify if the extracted figure 
    is actually an architecture diagram and not just a qualitative result.
    """
    try:
        # Initialize OpenAI client pointing to OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        base64_image = encode_image_to_base64(image)
        
        # We use a reliable free vision model on OpenRouter
        # Options: "google/gemini-2.0-flash-exp:free", "qwen/qwen-2-vl-72b-instruct", etc.
        # "openrouter/free" can also work but explicitly naming a free vision model is safer.
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-11b-vision-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this image from a research paper. Is it a neural network architecture diagram, system framework, or pipeline overview? Answer with only 'yes' or 'no'."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=10,
            temperature=0.0
        )
        text = response.choices[0].message.content.strip().lower()
        return 'yes' in text
    except Exception as e:
        print(f"  API Error during classification: {e}")
        # If API fails (e.g. rate limit), return True so we don't lose the diagram
        return True 

def get_figure_bbox(page, caption_bbox):
    """
    Groups vector graphics and bitmaps that are physically located above 
    the caption to form a complete bounding box for the entire figure.
    """
    gfx_rects = []
    
    # 1. Get all vector drawings (lines, boxes, shapes)
    for d in page.get_drawings():
        gfx_rects.append(d["rect"])
        
    # 2. Get all bitmap image fragments
    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            gfx_rects.append(fitz.Rect(r))
            
    # Keep graphics strictly above or overlapping the caption
    fig_graphics = [r for r in gfx_rects if r.y1 <= caption_bbox.y1 + 10]
    
    if not fig_graphics:
        # Fallback if no graphics detected: take the whole top region
        return fitz.Rect(0, max(0, caption_bbox.y0 - 300), page.rect.width, caption_bbox.y1 + 10)
        
    # Sort from bottom (closest to caption) to top
    fig_graphics.sort(key=lambda r: r.y1, reverse=True)
    
    # Cluster graphics to avoid capturing a second figure higher up on the same page
    filtered_graphics = []
    current_y0 = caption_bbox.y0
    
    for r in fig_graphics:
        # If there's a huge vertical gap (> 150 points), it's likely a different block
        if current_y0 - r.y1 > 150: 
            break
        filtered_graphics.append(r)
        current_y0 = min(current_y0, r.y0)
        
    if not filtered_graphics:
        filtered_graphics = fig_graphics
        
    # Create a union bounding box of all related graphics and the caption itself
    fig_bbox = fitz.Rect(caption_bbox)
    for r in filtered_graphics:
        fig_bbox |= r
        
    # Add a comfortable padding around the figure
    fig_bbox.x0 = max(0, fig_bbox.x0 - 15)
    fig_bbox.y0 = max(0, fig_bbox.y0 - 15)
    fig_bbox.x1 = min(page.rect.width, fig_bbox.x1 + 15)
    fig_bbox.y1 = min(page.rect.height, fig_bbox.y1 + 15)
    
    return fig_bbox

def extract_diagrams(pdf_dir, output_dir, api_key=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Keywords in captions that strongly suggest an architecture/pipeline diagram
    keywords = ["architecture", "framework", "overview", "pipeline", "method"]

    for filename in os.listdir(pdf_dir):
        if not filename.lower().endswith(".pdf"):
            continue
            
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"\nProcessing: {filename}")
        
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"  Failed to open {filename}: {e}")
            continue

        diagram_count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            try:
                blocks = page.get_text("dict")["blocks"]
            except Exception:
                continue
                
            for block in blocks:
                if block["type"] != 0: # Not a text block
                    continue
                    
                # Extract text from the block
                text = "".join([span["text"] for line in block["lines"] for span in line["spans"]])
                text = text.replace("\n", " ").strip()
                text_lower = text.lower()
                
                # Identify if this block is a Figure caption
                if re.match(r"^fig(?:ure)?\.?\s*\d+", text_lower):
                    # Check if it contains our target keywords
                    if any(k in text_lower for k in keywords):
                        caption_bbox = fitz.Rect(block["bbox"])
                        
                        # Find the full bounding box of the figure (graphics + caption)
                        fig_bbox = get_figure_bbox(page, caption_bbox)
                        
                        try:
                            # Render this specific region of the page at high resolution
                            pix = page.get_pixmap(clip=fig_bbox, dpi=300)
                            image_bytes = pix.tobytes("png")
                            image = Image.open(io.BytesIO(image_bytes))
                            
                            is_valid = True
                            if api_key:
                                print(f"  Found potential diagram on page {page_num+1}. Verifying with OpenRouter...")
                                is_valid = is_architecture_diagram_openrouter(image, api_key)
                                time.sleep(1) # Rate limit for free models
                                
                            if is_valid:
                                diagram_count += 1
                                out_name = f"{os.path.splitext(filename)[0]}_arch_{diagram_count}.png"
                                out_path = os.path.join(output_dir, out_name)
                                image.save(out_path, "PNG")
                                print(f"  -> Saved real architecture diagram: {out_name}")
                            else:
                                print(f"  -> OpenRouter rejected figure on page {page_num+1} as it's not a diagram.")
                                
                        except Exception as e:
                            print(f"  Error rendering figure on page {page_num+1}: {e}")
                            
        print(f"  Total true architecture diagrams found: {diagram_count}")

if __name__ == "__main__":
    PDF_DIRECTORY = "papers"
    OUTPUT_DIRECTORY = "architecture_diagrams"
    
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", None)
    
    if OPENROUTER_API_KEY:
        print("Using Layout Heuristics + OpenRouter Vision for perfect extraction...")
    else:
        print("Using Layout Heuristics for extraction. (Set OPENROUTER_API_KEY to filter false positives)")
        
    print("-" * 50)
    extract_diagrams(PDF_DIRECTORY, OUTPUT_DIRECTORY, OPENROUTER_API_KEY)
