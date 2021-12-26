from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from uatg.instruction_constants import base_reg_file, load_store_instructions, bit_walker
from typing import Dict, List, Union, Any
import re
import os
import random
class uatg_caches_dcache_fill(IPlugin):
	
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
        	
        def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        	asm_main="\n\tfence\n\tli t0, 77\n\tli t3, {0}\n\tla t2, rvtest_data" .format(self.sets * self.ways)
        	asm_loop1="\n\tloop1:\n\tsw t0, 0(t2)\n\taddi t2, t2,64\n\tbeq t4, t3, asm_nop\n\taddi t4, t4, 1\n\tj loop1\n\t".format(self.word_size * self.block_size)
        	asm_nop="\n\tnop\n\t"
       	for i in range(self.fb_size * 2):
            		asm_loop2 += sw t0, {0}(t2).format(32 * (i + 1))
            	asm_end="\n\tend:\n\tnop\n\tfence.i\n\t"
            	
            	asm_code=asm_main+asm_loop1+asm_nop+asm_loop2+asm_end
            	compile_macros=[]
            	
        	asm_data = '\nrvtest_data:\n'
                
                for i in range (self.block_size * self.sets * self.ways*2):
            		asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(16**8))

                return({'asm_code': asm_code,
                    'asm_data': asm_data,
                    'asm_sig': '',
                    'compile_macros': compile_macros})
                    
         def check_log(self, log_file_path, reports_dir):
       	f=open(log_file_path,'r')
       	log_file=f.read()
       	f.close()
       	test_report={"cache_dcache_fillbuffer:"{'Doc':"ASM should fill the fillbuffer of size {0}.This report verifies that.".format(self.fb_size),'Execution status':''}}
       	
       	
       def def generate_covergroups(self, config_file) -> str:
        sv = ""
        return sv    
       	
      
       	
        	
