#!/usr/bin/env python3
"""
Script tạo file laser.png đỏ rực, không có màu tối
"""

import pygame

def create_laser_image():
    """Tạo file laser.png"""
    pygame.init()
    
    width = 25
    height = 8
    laser_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Gradient đỏ rực từ sáng -> nhạt, không màu tối
    colors = [
        (255, 0, 0, 255),    # Đỏ sáng rực
        (255, 50, 50, 220),  # Đỏ tươi
        (255, 80, 80, 180),  # Đỏ nhạt hơn
        (255, 120, 120, 120) # Hồng nhạt
    ]
    
    # Vẽ laser ngang
    for i, color in enumerate(colors):
        size = height - i * 2
        if size > 0:
            x = 0
            y = (height - size) // 2
            pygame.draw.rect(laser_surface, color, (x, y, width, size), border_radius=2)
    
    # Thêm glow xung quanh
    glow_surface = pygame.Surface((width + 6, height + 6), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, (255, 50, 50, 100), (0, 0, width + 6, height + 6), border_radius=4)
    laser_surface.blit(glow_surface, (-3, -3))
    
    pygame.image.save(laser_surface, 'laser.png')
    print("✅ Đã tạo file laser.png đỏ rực, không màu đen giữa!")

if __name__ == "__main__":
    create_laser_image()
    pygame.quit()
