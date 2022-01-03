from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from uatg.instruction_constants import base_reg_file, load_store_instructions, bit_walker
from typing import Dict, List, Union, Any
import re
import os
import random
class uatg_caches_dcache_fillbuffers(IPlugin):
	
	def __init__(self) -> None:
		super().__init__()
        	self.sets=64
        	self.word_size=8
        	self.block_size=8
        	self.ways=4
        	self.fb_size=9
        	
        def execute(self,core_yaml,isa_yaml):
        	d_cache=core_yaml['dcache_configuration']
        	d_cache_en=d_cache['instantiate']
        	self.sets=d_cache['sets']
        	self.word_size=d_cache['word_size']
        	self.block_size=d_cache['block_size']
        	self.ways=d_cache['ways']
        	self.fb_size=d_cache['fb_size']
		return True
        	
        def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        	asm_main="\n\tli t1, 77\n\tli t3, {0}\n\tla t2, rvtest_data\n" .format(self.sets * self.ways)
        	asm_loop1="loop1:\n\tsd  t1,t8(x10)\n\taddi  t8,t8,64\n\tbeq  t8,t4,loop2\n\tj loop1\n"
        	asm_loop="loop2:\n\taddi t3,t3,1\n\tli t8,0\n\tbeq  t3,{0},end\n\tj loop1\n".format(self.sets)
        	asm_nop="asm_nop:\nnop\n\t"
        	asm_loop2=""
        	for i in range(self.fb_size ):
        		asm_loop2 += "\nsw t1, {0}(t2)\n".format(32 * (i + 1))
        	asm_end="\nend:\n\tnop\n\tfence.i\n\t"
        	asm_code=asm_main+asm_loop1+asm_loop+asm_nop+asm_loop2+asm_end
        	compile_macros=[]
        	asm_data = '\nrvtest_data:\n'
        	for i in range (self.block_size * self.sets * self.ways*2):
        		asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(2**32))
        	return[{'asm_code': asm_code,'asm_data': asm_data,'asm_sig': '','compile_macros': compile_macros}]
                    
                    
         def check_log(self, log_file_path, reports_dir)-> Bool:
      		return False
       	
         def generate_covergroups(self, config_file) -> Str:
        	sv = ""
        	return sv    
       	
      
       	
        	
