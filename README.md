# Final Project - PHYS 4041
This project uses parralel tempering on the ising model. It is only done in 
2D because the curse of dimensionality would make complexity much to hard 
to run on a single computer. Regardless the program still runs in parralel for a single
node with shared memory.  

NOTE: The library used for parrellization only works on linux and macOS machines. 
Windows is still in experimental.  


Note the parrelleization is only useful when having the walkers go on long walks. 
Meaning the compute time is longer than the queuing time. 
## Set up 

Note parralel execution only works on Linux and MacOS. 
From terminal window do the following commands :
1) `conda create --name <env>  
python=3.8.5 numpy=1.19.* pandas matplotlib scipy`
Where `<env>` is your environment name. Then from the commmand line type: 
2) `conda activate <env>`
3) `pip install ray==1.0.1`

The environment set up is now complete. 


## To run : 

Specify the inputs given by the inputs dictionary. Make sure to have made the directory 
`./tempering_results/` as a location to save the data. Otherwise you will have errors. 
Specify the inputs in a dictionary by the driver script on `parralel_tempering.py`. I've
included seed values for reproducibility. 

It is **highly advised** to make the number of walkers the same as the number of virutal cores on 
your computer. 

## Notes: 

Using boundary conditions for the ends of the Edwards -  Spin Glass model. 
