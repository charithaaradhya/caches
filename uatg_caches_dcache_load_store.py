from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from uatg.instruction_constants import base_reg_file, load_store_instructions, bit_walker
from typing import Dict, List, Union, Any
import re
import os
import random
class uatg_caches_dcache_load_store(IPlugin):
	
	def __init__(self) -> None:
		super().__init__()
        	
        def execute(self,core_yaml,isa_yaml):
        	d_cache=core_yaml['dcache_configuration']
        	d_cache_en=d_cache['instantiate']
        	self.sets=d_cache['sets']
        	self.word_size=d_cache['word_size']
        	self.block_size=d_cache['block_size']
        	self.ways=d_cache['ways']
		return True
		
        def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        	asm_main="main:\n\tla x10,rvtest_data\n\tlui t2, 0xAAAAB\n\t addi t2,t2,xAAA\n"
        	asm_byte="check_byte:\n\tli t0, 0xAA\n\tsb t2, {0}(x10)\n\tlbu t3, {0}(x10)\n\tbne a2, t3, end\n\tli t0, 0xFFFFFFFFFFFFFFAA \n\tlb t3, {0}(x10) \n\tbne t3, t0, end\n".format(64* 0)
        	asm_half_word="check_half_word:\n\tlui a2, 0xAAAA\n\tsh t2, {0}(x10)\n\t lhu t3, {0}(x10)\n\t bne t0, t3, end\n\tli t0, 0xFFFFFFFFFFFFAAAA\n\tlh t3, {0}(x10)\n\tbne t3, a2, end\n".format(64 * 1)
        	asm_word="check_word:\n\tlui a2, 0xAAAAA\n\tlui a2,0XAA\n\tsw t2, {0}(x10)\n\t lwu t3, {0}(x10)\n\t bne a2, t3, end\n\tli a2, 0xFFFFFFFFAAAAAAAA\n\tlw t3, {0}(x10)\n\tbne t3, a2, end\n".format(64 * 2)
        	asm_double="check_double:\n\tlui a2, 0xAAAAB\n\taddi a2,a2,0XAAA \n\tsd t2, {0}(x10)\n\tld t3, {0}(x10)\n\tbne a2, t3, end\n\tli a2, 0xAAAAAAAAAAAAAAAA\n\tld t3, {0}(x10) \n\tbne t3, a2, end\n".format(64 * 3)
        	asm_end="end:\n\tnop\n\tfence.i\n"
        	asm_code=asm_main+asm_byte+asm_half_word+asm_word+asm_double+asm_end
        	compile_macros=[]
        	asm_data = '\nrvtest_data:\n'
        	for i in range (self.block_size * self.sets * self.ways*2):
        		asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(2**32))
        	return[{'asm_code': asm_code,'asm_data': asm_data,'asm_sig': '','compile_macros': compile_macros}]
        
       	
                    
       def check_log(self, log_file_path, reports_dir)-> Bool:
       		return False
       	
       def def generate_covergroups(self, config_file) -> Str:
       		sv = ""
        	return sv       
