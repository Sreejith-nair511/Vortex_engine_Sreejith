import pygame as pg
import moderngl as mgl
import sys
import traceback
from settings import *
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures


class VoxelEngine:
    def __init__(self):
        print("Initializing VoxelEngine...")
        # Initialize Pygame
        pg.init()
        
        # Set OpenGL attributes
        print("Setting OpenGL attributes...")
        self.set_gl_attributes()
        
        # Create window and OpenGL context
        print("Creating window...")
        self.create_window()
        
        # Initialize game state
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        
        # Set mouse properties
        print("Setting up mouse...")
        self.setup_mouse()
        
        # Initialize game objects
        self.is_running = True
        print("Starting initialization...")
        self.on_init()
    
    def set_gl_attributes(self):
        """Set OpenGL context attributes"""
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)
    
    def create_window(self):
        """Create game window and initialize OpenGL context"""
        self.screen = pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        
        # Enable OpenGL flags
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'
    
    def setup_mouse(self):
        """Configure mouse settings"""
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
    
    def on_init(self):
        """Initialize game objects"""
        try:
            print("Loading textures...")
            self.textures = Textures(self)
            
            print("Creating player...")
            self.player = Player(self)
            
            print("Setting up shader program...")
            self.shader_program = ShaderProgram(self)
            
            print("Creating scene...")
            self.scene = Scene(self)
            
            print("Initialization complete!")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            self.is_running = False
    
    def update(self):
        """Update game state"""
        try:
            self.player.update()
            self.shader_program.update()
            self.scene.update()
            
            # Update timing
            self.delta_time = self.clock.tick()
            self.time = pg.time.get_ticks() * 0.001
            
            # Update FPS display
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.0f}')
        except Exception as e:
            print(f"Error during update: {str(e)}")
            traceback.print_exc()
            self.is_running = False
    
    def render(self):
        """Render game scene"""
        try:
            self.ctx.clear(color=BG_COLOR)
            self.scene.render()
            pg.display.flip()
        except Exception as e:
            print(f"Error during rendering: {str(e)}")
            traceback.print_exc()
            self.is_running = False
    
    def handle_events(self):
        """Process game events"""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            try:
                self.player.handle_event(event=event)
            except Exception as e:
                print(f"Error handling event: {str(e)}")
                traceback.print_exc()
    
    def run(self):
        """Main game loop"""
        print("Starting game loop...")
        try:
            while self.is_running:
                self.handle_events()
                self.update()
                self.render()
        except Exception as e:
            print(f"Error during game execution: {str(e)}")
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    try:
        print("Starting application...")
        app = VoxelEngine()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
        pg.quit()
        sys.exit(1)