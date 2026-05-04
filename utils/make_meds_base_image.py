from PIL import Image, ImageTk

if __name__ == "__main__":
    base = Image.new("RGBA", (394, 261), color=(0, 0, 0, 0))
    
    sBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    syringes = Image.open("media/1 Syringe.png").resize((128, 128))
    sBase.alpha_composite(syringes)

    mBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    meds = Image.open("media/2 Med Kit.png").resize((128, 128))
    mBase.alpha_composite(meds)
    
    pBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    phoenix = Image.open("media/3 Phoenix Kit.png").resize((128, 128))
    pBase.alpha_composite(phoenix)

    cBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    cells = Image.open("media/4 Shield Cell.png").resize((128, 128))
    cBase.alpha_composite(cells)

    bBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    batts = Image.open("media/5 Shield Battery.png").resize((128, 128))
    bBase.alpha_composite(batts)

    uBase = Image.new("RGBA", (128, 128), color=(25, 26, 27, 80))
    ults = Image.open("media/6 Ultimate Accelerant.png").resize((128, 128))
    uBase.alpha_composite(ults)

    base.alpha_composite(sBase, dest=(0, 0))
    base.alpha_composite(mBase, dest=(133, 0))
    base.alpha_composite(pBase, dest=(266, 0))
    base.alpha_composite(cBase, dest=(0, 133))
    base.alpha_composite(bBase, dest=(133, 133))
    base.alpha_composite(uBase, dest=(266, 133))

    base.save("media/base.png")