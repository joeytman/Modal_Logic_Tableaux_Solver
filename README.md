# Modal_Logic_Tableaux_Solver
A python tool to decide satisfiability of modal formulas, and if satisfiable, visualize them.

I'm creating this as part of my final paper for my Modal Logic class at UC Berkeley. There was no specific prompt or topic we needed to write about, merely the specification that whatever we do must relate to modal logic in significant ways and be conceptually interesting; thus, I decided to write this as a tool to help me quickly visualize models for many formulas in order to analyze and model the world view of various political figures, writing about its creation and highlighting some various applications as my paper's topic.

This tool obviously does not exhaustively find.visualize all possible satisfying models (infinitely many), but more significantly, it does not necessarily find all 

# Instructions:
1. Install python 3 and the following library dependencies: networkx, matplotlib
2. Download the zip file from this page or clone it through git
3. Navigate within the terminal to the directory you downloaded the files to
4. From inside the folder, run the following (items within [brackets] are optional:
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

# Disclaimer
If you're a developer reading this and you'd like to use this tool for anything, feel free. If you want to copy all of my code and add it to something you're working on, go for it, just credit me somewhere and drop me a star. 
