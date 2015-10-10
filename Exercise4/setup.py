from distutils.core import setup  
import py2exe  
import glob
  
setup(windows=['TetrisWindow.py'],
      data_files=[("Images", glob.glob("Images\\*.jpg")),
                  ("FontEffects", glob.glob("FontEffects\\*.fx")),
                  ("BackgroundEffects", glob.glob("BackgroundEffects\\*.fx")),
                  ("DLLs", glob.glob("C:\Users\MarkKC_Ma\Desktop\KoanSDK\DLLs\\*"))], # Copy all the DLLs needed when runtime
      
      # only search __init__
      package_dir={'Widgets': 'C:\Users\MarkKC_Ma\Desktop\KoanSDK\Widgets',
                   'koan': 'C:\Users\MarkKC_Ma\Desktop\KoanSDK\koan'},
      # doesn't recursively search all the packages, so we have to add them by ourselves
      packages=['Widgets', 'koan', 'koan.platform', 'koan.renderer', 'koan.img', 'koan.animate'],
      )  


# python setup.py py2exe -O2 -b 2
