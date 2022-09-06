class SignalMeta(type):                                                         
     def __new__(cls, what, bases=None, dict=None):                              
         print(dict)                                                             
         if 'print_period' in dict:                                              
             print('Great you have print_period')                                
         else:                                                                   
             raise Exception('print_period missing')                             
         new_dict= {}                                                            
         for key, val in dict.items():                                           
              new_dict['pp_'+key] = val
         return type.__new__(cls, what, bases, new_dict)                         
                                                                                 
 class SignalWithMetaSignal(metaclass=SignalMeta):                               
     def print_period(self):                                                     
         pass