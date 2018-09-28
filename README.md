# Modal_Logic_Tableaux_Solver
A python tool to decide satisfiability of modal formulas, and if satisfiable, visualize them.

I'm creating this as part of my final paper for my Modal Logic class at UC Berkeley. There was no specific prompt or topic we needed to write about, merely the specification that whatever we do must relate to modal logic in significant ways and be conceptually interesting; thus, I decided to write this as a tool to help me quickly visualize models for many formulas in order to analyze and model the world view of various political figures, writing about its creation and highlighting some various applications as my paper's topic.

This tool obviously does not exhaustively find/visualize all possible satisfying models (infinitely many), but more significantly, it does not necessarily find all possible satisfying models that are unique through bisimulation reduction. This is not an exhaustive search and is not intended to be, as it seeks merely to provide a "yes" or "no" answer to the satisfiability question. The visualization of multiple models exists only to see a few examples of models that satisfy the formula in their own different ways.

Note that reflexive arrows are not drawn on the visualization but are still being properly processed. To ensure that your input is being treated correctly, ensure that the restrictions on relations that you specified appear in the terminal when you run the program.

# Instructions:
1. Install python 3 and the following library dependencies: networkx, matplotlib

2. Download the zip file from this page or clone it through git

3. Navigate within the terminal to the directory you downloaded the files to

4. From inside the folder, run the following (items within [brackets] are optional):

       python3 solver.py "<your-modal-formula-here>" [--novis] [--debug] [reflexive | symmetric | transitive]
        
   When writing the modal formula:
   
          all lowercase letters are treated as atomic
          
          "^" or "&" can be used for conjunction
          
          "|" is for disjunction
          
          "[]" or "B" are used for box operator
          
          "<>" or "D" are used for diamond operator
          
          ">" is used for implications
          
          "~" is used for negation
          
  The optional --novis flag makes the program only decide satisfiability of the given formula without visualizing it
  
  The optional --debug flag prints a verbose output to console as the program runs
  
  Additionally, you can add any combination (or none) of "reflexive", "symmetric", and "transitive" (no quotes) after your formula and any optional flags in order to impose restrictions on the frame's relations.
  
# Uses
There are quite a few uses of this program. One such use is to prove formulas -- if you want to prove <phi> on some frame, simply determine whether ~<phi> is satisfiable on that frame, as if it is not, then it must hold that phi is valid on all models based on that frame.

For instance, let's look at this instance of the 4 axiom, pretending we don't know anything about it: <><>p -> <>p
Maybe we want to start by seeing if this is satisfiable on unrestricted frames...
![Just enter this and see some examples](https://i.imgur.com/vW5AHNT.png)

Well, cool, it's satisfiable. Is it valid on all models on all frames?
![Definitely not, as here is a counter-example](https://i.imgur.com/b1oLVDI.png)

The program just provided a counter-example, so it must not be.
However, what if we search for a counter-example on frames that are reflexive and transitive?
![Unsurprisingly, there is no way to satisfy the negation of <><>p -> <>p on these frames](https://i.imgur.com/8R5WtNE.png) Unsurprisingly, there is no way to satisfy the negation of <><>p -> <>p on these frames. Hence, we can conclude that <><>p -> <>p is valid in all worlds with reflexive and transitive frames.

Hopefully this gives you a good idea of some use that can be had with this, and please note any bugs you find as I'll do my best to fix them asap.

# Disclaimer
If you're a developer reading this and you'd like to use this tool for anything, feel free. If you want to copy all of my code and add it to something you're working on, go for it, just credit me somewhere and drop me a star. 

# Credits
I want to thank Marcin Cuber for open source-ing his masters thesis, the repo of which can be found [Here](https://github.com/marcincuber). I used a lot of his code for writing the parser for this, which otherwise would have taken me so much longer.
