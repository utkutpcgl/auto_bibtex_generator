# auto_bibtex_generator
Generates bibtex automatically when the author and title information is available. This script is the second part of a 2 step auto bibtex generation process. 

# AUTOMATIC BIBTEX GENERATION FROM TEXT

## Step 1:
You can feed a text to this GPT (here: https://chatgpt.com/g/g-qkXOfDbtO-text-to-reference-python-list-and-rewrite) to output the required input for this repository. The output will be in this format:

    raw_papers = [
        ("Howard", "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications", "howard2017mobilenets"),
        ("Tan and Le", "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks", "tan2019efficientnet"),
        ("He", "Deep Residual Learning for Image Recognition", "he2016deep"),
        ("Huang", "Densely Connected Convolutional Networks", "huang2017densely"),
        ("Wang", "Deep High-Resolution Representation Learning for Visual Recognition", "wang2019deep"),
        ("Dai", "Deformable Convolutional Networks", "dai2017deformable")
    ]

## Step 2:
Then you can change the raw_papers variable in get_bib_arxiv.py. When you run the code it will print the BibTeX references.
