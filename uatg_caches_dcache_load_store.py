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
        	
        def execute(self,core_yaml,isa_yaml):
        	d_cache=core_yaml['dcache_configuration']
        	d_cache_en=d_cache['instantiate']
        	self.sets=d_cache['sets']
        	self.word_size=d_cache['word_size']
        	self.block_size=d_cache['block_size']
        	self.ways=d_cache['ways']
		
        def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        	asm_main="main:\n\tli t1, 8000\n\tli t2, 0xAAAAAAAAAAAAAAAA\n\tli t4, 0x1111"
        	asm_byte="check_byte:\n\tli t0, 0xAA\n\tsb t2, {0}(t1)\n\tlbu t3, {0}(t1)\n\tbne a2, t3, end\n\tli t0,0xFFFFFFFFFFFFFFAA\n\tld t3, {0}(t1) \n\tbne t3, t0, end\n".format(self._word_size * self._block_size * 1)
        	asm_half_word="check_half_word:\n\tli a2, 0xAAAA\n\tsh t2, {0}(t1)\n\t lhu t3, {0}(t1)\n\t bne t0, t3, end\n\tli t0, 0xFFFFFFFFFFFFAAAA\n\tlh t3, {0}(t1)\n\tbne t3, a2, end\n"   .format(self._word_size * self._block_size * 2)
        	asm_word="check_word:\n\tli a2, 0xAAAAAAAA\n\tsw t2, {0}(t1)\n\t lwu t3, {0}(t1)\n\t bne a2, t3, end\n\tli a2, 0xFFFFFFFFAAAAAAAA\n\tlw t3, {0}(t1)\n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 3)
        	asm_double="check_double:\n\tli a2, 0xAAAAAAAAAAAAAAAA\n\tsd t2, {0}(t1)\n\tld t3, {0}(t1)\n\tbne a2, t3, end\n\tli a2, 0xAAAAAAAAAAAAAAAA\n\tld t3, {0}(t1) \n\tbne t3, a2, end\n".format(self._word_size * self._block_size * 4)
		asm_end="end:\n\tnop\n\tfence.i\n""
        	asm=asm_main+asm_byte+asm_half_word+asm_word+asm_double+asm_end
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
       	test_report={"cache_dcache_dcache_load_Store:"{'Doc':"ASM should perform load and store operationson cache ",'Execution status':''}}
       	
       	
       	
       def def generate_covergroups(self, config_file) -> str:
       	sv = ""
        	return sv       
