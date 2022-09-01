import pygame
import colorsys
import time
import math
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)


def interp(inp, input_start, input_end, output_start, output_end):
    output = output_start + ((output_end - output_start) / (input_end - input_start)) * (inp - input_start)
    return output

def compute_mandelbrot(rect, mandel_range, max_it):

    if rect is not None:
        rect_xmin, rect_ymin = rect.topleft
        rect_xmax, rect_ymax = rect.bottomright

        xmin = interp(rect_xmin, 0, screen_rect.w, *mandel_range[0])
        xmax = interp(rect_xmax, 0, screen_rect.w, *mandel_range[0])
        ymin = interp(rect_ymin, 0, screen_rect.h, *mandel_range[1])
        ymax = interp(rect_ymax, 0, screen_rect.h, *mandel_range[1])
    else:
        ([xmin,xmax],[ymin,ymax]) = mandel_range

    # print(mandel_range)
    # print((xmin,xmax),(ymin,ymax))
    # print(rect_xmin, rect_ymin, rect_xmax, rect_ymax)
    # print()

    pixel_arr = pygame.PixelArray(screen)

    max_iter = max_it
    for px in range(screen_rect.w):
        for py in range(screen_rect.h):
            x0 = interp(px, 0, screen_rect.w, xmin,xmax)
            y0 = interp(py, 0, screen_rect.h, ymin,ymax)

            x = x2 = 0.0
            y = y2 = 0.0
            it = 0

            while (x2 + y2 <= 4 and it < max_iter):
                y = (x+x)*y+y0
                x = x2-y2+x0
                x2=x*x
                y2=y*y
                it += 1
            
            # color = (it / max_iter, 0.8, 0.8 if it<max_iter else 0)
            # c = tuple([int(c*255) for c in colorsys.hsv_to_rgb(*color)])
            a = 0.1
            n = it
            # interesting colouring formula
            c = (0.5 * math.sin(a * n + 4.188) + 0.5) * 128 + 127, \
                (0.5 * math.sin(a * n) + 0.5) * 128 + 127, \
                (0.5 * math.sin(a * n + 2.094) + 0.5) * 128 + 127
                
            pixel_arr[px,py] = c
            # pixel_arr[px,(screen_rect.h-1)-py] = c

    pixel_arr.close()

    return ([xmin,xmax], [ymin,ymax])


def main():

    mandel_range = ([-2.0,0.47],[-1.12,1.12])
    zoom = screen_rect
    it = 32

    screen.fill(BLACK)
    compute_mandelbrot(zoom, mandel_range, it)
    pygame.display.flip()

    mouse_state = 0
    click = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.key.get_pressed()[pygame.K_UP]:
            it += 16
            mandel_range = compute_mandelbrot(None, mandel_range, it)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            it = max (1,it-16)
            mandel_range = compute_mandelbrot(None, mandel_range, it)

        next_step = False
        curr_mouse = pygame.mouse.get_pressed()[0]
        if curr_mouse != mouse_state:
            mouse_state = curr_mouse
            if curr_mouse:
                m1 = pygame.mouse.get_pos()
                click = True
            elif click:
                m2 = pygame.mouse.get_pos()
                next_step = True
                click = False
        
        if next_step:
            next_step = False
            w = m2[0]-m1[0]
            h = m2[1]-m1[1]
            zoom = pygame.Rect(m1,(w,h))

            #clear the screen
            screen.fill(BLACK)

            t = time.time()
            mandel_range = compute_mandelbrot(zoom, mandel_range, it)
            print(time.time() - t)
            

        # flip() updates the screen to make our changes visible
        pygame.display.flip()

        pygame.image.save(screen, "mandelbrot_set.png")
    
    pygame.quit()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen_size = (600, 600)
    
    # create a window
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    
    # clock is used to set a max fps
    clock = pygame.time.Clock()  
    main()