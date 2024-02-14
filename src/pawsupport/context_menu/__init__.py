from ..pdf_tools.array_pdfs import array

from context_menu import menus

fc = menus.FastCommand('Example Fast Command 1', type='FILES', command='echo Hello')
fc.compile()