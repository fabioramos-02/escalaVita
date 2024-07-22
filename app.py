import cv2
import numpy as np

# Função para carregar e redimensionar as imagens
def load_and_resize_image(path, width=None, height=None):
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Não foi possível carregar a imagem: {path}")
    if width and height:
        image = cv2.resize(image, (width, height))
    return image

# Função para extrair a cor média de uma região de interesse (ROI)
def extract_color_from_roi(image, roi):
    x1, x2, y1, y2 = roi
    roi_image = image[y1:y2, x1:x2]
    average_color = cv2.mean(roi_image)[:3]
    return np.array(average_color, dtype=np.uint8)

# Coordenadas das regiões de interesse (ROIs) para cada cor da escala VITA
vita_scale_rois = {
    "A1": (50, 80, 165, 220),
    "A2": (100, 130, 165, 220),
    "A3": (140, 170, 165, 220),
    "A3.5": (180, 210, 165, 220),
    "A4": (225, 260, 165, 220),
    "B1": (270, 300, 165, 220),
    "B2": (310, 350, 165, 220),
    "B3": (360, 390, 165, 220),
    "B4": (400, 430, 165, 220),
    "C1": (440, 470, 165, 220),
    "C2": (480, 520, 165, 220),
    "C3": (530, 560, 165, 220),
    "C4": (570, 600, 165, 220),
    "D2": (610, 640, 165, 220),
    "D3": (650, 690, 165, 220),
    "D4": (700, 730, 165, 220)
}

# Carregar a imagem da escala VITA
vita_scale_image = load_and_resize_image('scale_image.png')

# Extrair as cores da escala VITA a partir das ROIs
vita_scale_colors = {name: extract_color_from_roi(vita_scale_image, roi) for name, roi in vita_scale_rois.items()}

# Criar uma imagem para mostrar as cores extraídas
height = 50
width = 300
margin = 10
num_colors = len(vita_scale_colors)
image = np.ones((num_colors * (height + margin), width, 3), dtype=np.uint8) * 255

# Desenhar cada cor na imagem
for i, (color_name, color_value) in enumerate(vita_scale_colors.items()):
    start_y = i * (height + margin)
    end_y = start_y + height
    cv2.rectangle(image, (0, start_y), (width, end_y), color_value.tolist(), -1)
    cv2.putText(image, color_name, (10, start_y + height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

# Salvar a imagem
cv2.imwrite('vita_scale_colors_extracted.png', image)
print('A imagem com as cores extraídas foi salva como vita_scale_colors_extracted.png.')

# Função para calcular a diferença de cor
def color_difference(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

# Função para encontrar a cor mais próxima na escala VITA
def find_closest_color(tooth_color, vita_scale_colors):
    closest_color = None
    min_diff = float('inf')
    for color_name, color_value in vita_scale_colors.items():
        diff = color_difference(tooth_color, color_value)
        if diff < min_diff:
            min_diff = diff
            closest_color = color_name
    return closest_color

# Carregar a imagem do sorriso
sorriso_image = load_and_resize_image('smiles/feio.jpg')

# Definir a ROI do sorriso (exemplo simples, ajustar conforme necessário)
sorriso_roi = (50, sorriso_image.shape[1] - 50, 50, sorriso_image.shape[0] - 50)

# Extrair a cor média da ROI do sorriso
average_color = extract_color_from_roi(sorriso_image, sorriso_roi)

# Desenhar a ROI na imagem do sorriso
x1, x2, y1, y2 = sorriso_roi
sorriso_image_with_roi = sorriso_image.copy()
cv2.rectangle(sorriso_image_with_roi, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Salvar a imagem do sorriso com a ROI destacada
cv2.imwrite('sorriso_with_roi.png', sorriso_image_with_roi)
print('A imagem do sorriso com a ROI destacada foi salva como sorriso_with_roi.png.')

# Encontrar a cor mais próxima na escala VITA
closest_color = find_closest_color(average_color, vita_scale_colors)

print(f'A cor mais próxima na escala VITA é: {closest_color}')
