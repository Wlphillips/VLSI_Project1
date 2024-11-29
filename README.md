# VLSI_Project1
Project 1 for replicating QM Method in Python

Inputs (.i) = # of bits,
2 inputs = 4 possible minterms,
3 inputs = 8,
4 inputs = 16,
etc.

Input4.pla = input file, Input4_minimized.pla = output file, Input4_terminal_output = terminal debugging output.



Some of the implementation challenges that I ran into were mostly related to parsing the input data and making sure that everything was read correctly from the file and trying to eliminate the duplicate covers in the output file. 

The parsing data problem took me a while because I couldnt figure out why the information wasn't being read correctly. I had a bit of difficulty with the PLA format but eventually got it down and was able to read everything correctly.

The Duplicate issue was one that really stumped me, mostly because every time I tried to implement duplicate checking to reduce cover redundancy, it would influence the output and make it incorrect. I could never get a solution that was both correct and rid of duplicates, so between the two, I'd rather be correct and have duplicates.

Below is the basic verification of functionality. It shows the correct output but still has duplicate covers.

![Basic_verification_of_Functionality](https://github.com/user-attachments/assets/55f3566c-2b27-4518-9a74-f210a8d154ea)


