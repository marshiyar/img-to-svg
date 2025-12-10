import os
import argparse
import sys
import base64
from io import BytesIO
from PIL import Image, ImageEnhance
import vtracer

def preprocess_image(img, enhance=True):
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    if enhance:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
    
    return img

def create_hybrid_svg(img, output_path):
    buffer = BytesIO()
    img.save(buffer, format='PNG', optimize=False, compress_level=1)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    width, height = img.size
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" 
         xlink:href="data:image/png;base64,{img_base64}"/>
</svg>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return True

def convert_to_svg(input_path, output_path=None, mode='maximum', hybrid=False):
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.svg"

    try:
        with Image.open(input_path) as img:
            if hybrid:
                create_hybrid_svg(img.copy(), output_path)
                return
            
            img = preprocess_image(img, enhance=True)
            temp_input = f"temp_{os.path.basename(input_path)}"
            img.save(temp_input, quality=100, optimize=False)

        quality_settings = {
            'maximum': {
                'filter_speckle': 0,
                'color_precision': 8,
                'layer_difference': 1,
                'corner_threshold': 30,
                'length_threshold': 1.0,
                'max_iterations': 20,
                'splice_threshold': 30,
                'path_precision': 6,
                'mode': 'spline',
            },
            'high': {
                'filter_speckle': 1,
                'color_precision': 7,
                'layer_difference': 5,
                'corner_threshold': 45,
                'length_threshold': 2.0,
                'max_iterations': 15,
                'splice_threshold': 40,
                'path_precision': 5,
                'mode': 'spline',
            },
            'medium': {
                'filter_speckle': 2,
                'color_precision': 6,
                'layer_difference': 10,
                'corner_threshold': 60,
                'length_threshold': 3.5,
                'max_iterations': 10,
                'splice_threshold': 45,
                'path_precision': 4,
                'mode': 'spline',
            },
            'fast': {
                'filter_speckle': 4,
                'color_precision': 5,
                'layer_difference': 20,
                'corner_threshold': 90,
                'length_threshold': 5.0,
                'max_iterations': 5,
                'splice_threshold': 60,
                'path_precision': 3,
                'mode': 'polygon',
            }
        }
        
        settings = quality_settings.get(mode, quality_settings['maximum'])
        
        vtracer.convert_image_to_svg_py(
            temp_input,
            output_path,
            colormode='color',
            hierarchical='stacked',
            mode=settings['mode'],
            filter_speckle=settings['filter_speckle'],
            color_precision=settings['color_precision'],
            layer_difference=settings['layer_difference'],
            corner_threshold=settings['corner_threshold'],
            length_threshold=settings['length_threshold'],
            max_iterations=settings['max_iterations'],
            splice_threshold=settings['splice_threshold'],
            path_precision=settings['path_precision']
        )
        
        if os.path.exists(temp_input):
            os.remove(temp_input)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        if 'temp_input' in locals() and os.path.exists(temp_input):
            os.remove(temp_input)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert images to SVG vectors.")
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("-o", "--output", help="Path to output SVG file", default=None)
    parser.add_argument("--mode", choices=['maximum', 'high', 'medium', 'fast'], 
                       default='maximum', help="Quality mode")
    parser.add_argument("--hybrid", action="store_true", 
                       help="Embed raster in SVG")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    
    convert_to_svg(args.input, args.output, args.mode, args.hybrid)

if __name__ == "__main__":
    main()
