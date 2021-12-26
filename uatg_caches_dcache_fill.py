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
        def execute(self,core_yaml,isa_yaml):
        	d_cache=core_yaml['dcache_configuration']
        	d_cache_en=d_cache['instantiate']
        	self.sets=d_cache['sets']
        	self.word_size=d_cache['word_size']
        	self.block_size=d_cache['block_size']
        	self.ways=d_cache['ways']
        def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        	asm_main="\tfence\n\tla x5,rvtest_data\n\tli t5,{0}\n\taddi t5,t5,1\n".format(self.sets)
        	asm_loop2="loop2:\n\taddi t3,t3,1\n\tbeq  t3,t5,end\n"
        	asm_loop1="loop1:\n\tsd  t1,0(x5)\n\taddi  t2,t2,1\n\tbneq  t2,{0},loop1\n\tj loop2\n".format(self.ways)
        	asm_end="\n\tend:\n\tnop\n"
        	asm=asm_main+asm_loop2+asm_loop1+end
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
       	test_report={"cache_dcache_try:"{'Doc':"ASM should fill the cache of size {0}.This report verifies that.".format(self.sets*self.ways*self.block_size*self.word_size),''Execution status':''}}
       	
       	
       	
      def def generate_covergroups(self, config_file) -> str:
        sv = ""
        return sv       
