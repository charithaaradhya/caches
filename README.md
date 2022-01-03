Caches:

This module contains python codes to generate assembly files for testing the data cache of the Chromite Core developed by InCore Semiconductors.

Here we test the following:
       1. Fill the cache completely based on the size mentioned in the core64.yaml input
       2. Try to fill the fill-buffer completely.
       3. Perform types of load/store access.
 1. Fill the cache completely based on the size mentioned in the core64.yaml input:
      >first we fill 64 bits of  data in cache completing one block
      >loop 1 fills each block until one set(4 ways) are filled
      >after one set it shifts to loop 2 where it will increment reg by 1 and returns back to loop1 to fill the next set
      >this will continue until all the sets(64sets) are filled.
      
 2. Try to fill the fill-buffer completely:
       >First we fill the cache completely 
       >Then we try to fill the fill-buffer through a series of store operation 
       Without any chance for opportunistic-release 
 3. Perform types of load/store access.
       >We load and store one byte signed and unsigned of data
       >We load and store half word of signed and unsigned data
       >We load and store a word of signed and unsigned data
       >We load and store double word of signed and unsigned data



       
       
       
Contributors:
Charitha T S <ts.charitha1@gmail.com>,Adithi K<>.

Attribution:
Vishweshwaran K <vishwa.kans07@gmail.com>, Karthik B K <bkkarthik@pesu.pes.edu>
