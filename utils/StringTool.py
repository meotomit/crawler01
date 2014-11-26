import unicodedata
import re
class StringTool :
    
    @staticmethod
    def remove_diacritic(input):
        '''
        Accept a unicode string, and return a normal string (bytes in Python 3)
        without any diacritical marks.
        '''
        return unicodedata.normalize('NFKD', input).replace(u'đ', 'd').replace(u'Đ', 'D').encode('ASCII', 'ignore')
    
    def remove_diacritic_utf8(self, input):
        '''
        Accept a unicode string, and return a normal string (bytes in Python 3)
        without any diacritical marks.
        '''
        return unicodedata.normalize('NFKD', unicode(input, 'utf-8').replace(u'\u0111', 'd').replace(u'\u0110', 'D')).encode('ASCII', 'ignore')
    
    @staticmethod
    def normalnize_file_name(input) :
        '''
        Normalize file name : remove diacritic, replace space or expecial character by hyphen
        '''
        NORMAL_CHAR = re.compile('([^a-zA-Z0-9])+')
        
        input = StringTool.remove_diacritic(input)
        input = input.lower()
        
        input = NORMAL_CHAR.sub('-', input)
        if input.endswith('-') :
            input = input[0:-1]

        if input.startswith('-') :
            input = input[1:]
        
        return input
    
    @staticmethod
    def normalnize_file_name_utf8(input) :
        '''
        Normalize file name : remove diacritic, replace space or expecial character by hyphen
        '''
        NORMAL_CHAR = re.compile('([^a-zA-Z0-9])+')
        
        input = StringTool.remove_diacritic_utf8(input)
        input = input.lower()
        
        input = NORMAL_CHAR.sub('-', input)
        if input.endswith('-') :
            input = input[0:-1]

        if input.startswith('-') :
            input = input[1:]
        
        return input
    
    @staticmethod
    def encodeUtf8(input):
        if isinstance(input, unicode):
            input = input.encode('utf-8')
    
    @staticmethod
    def convert_to_wap_content(content):
        '''
            Convert to wap content
        '''
#        import pdb
#        pdb.set_trace()
        # Replace new line --> @br@
        content = re.sub("<br\s*/>", "@br@@br@", content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        content = re.sub('(</div>)', '', content, 0, re.M | re.I | re.DOTALL)
        
        # keep p tag without style
        content = re.sub("<p.*?>", "@p_tag@", content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        content = re.sub('(</p>)', '@end_p_tag@', content, 0, re.M | re.I | re.DOTALL)
        
        # replace empty p tag
        content = re.sub("@p_tag@\W*@end_p_tag@", "", content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        
        # replace new line tags
        content = re.sub("<(div|tr|li).*?>", "@br@@br@", content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        #content = re.sub("<p.*?>", "@ptag@", content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        
        # Normalize image
        imagePattern = r'''<img[^>].*?src\s*=\s*[\"']([^'\"]+?)[\"'].*?>'''
        imageReplacement = r'''@img@ src="\1" with="99%" @end_img@ '''
        content = re.sub(imagePattern, imageReplacement, content, 0, re.MULTILINE | re.DOTALL | re.IGNORECASE)        
        
        # Keep bold tag
        content = content.replace('<strong>', '@strong_tag@')
        content = content.replace('</strong>', '@end_strong_tag@')
        
        # Keep bold italic tag
        content = content.replace('<em>', '@em_tag@')
        content = content.replace('</em>', '@end_em_tag@')
        
        # Replace script tag
        content = re.sub("<script[^>].*?>.*?</script>", "", content, 0 , re.MULTILINE | re.DOTALL | re.IGNORECASE | re.UNICODE)
        
        # Replace other tag
        content = re.sub("<.*?>", "", content, 0 , re.MULTILINE | re.DOTALL | re.IGNORECASE)
        
        # Replace special chars
        #content = content.replace("\n", " ")
        #content = content.replace("\t", " ")
        #content = content.replace("\r", " ")
        content = content.replace('  ', '')
        
        try:
            content = content.replace(u'@br@ @br@', '@br@@br@')
            content = content.replace(u'@br@ @br@', '@br@@br@')
            content = content.replace(u'@br@  @br@', '@br@@br@')
            content = content.replace('@br@ @br@', '@br@@br@')
            content = re.sub('@br@@br@\W*@br@@br@', '@br@@br@', content)
        except Exception, e:
            print e.strerror
        
        # Thay 4 @br@ thanh 2 @br@
        content = re.sub('(@br@@br@)+', '@br@@br@', content)
        
#        import pdb
#        pdb.set_trace()

        # loai bo the the strong thừa
        content = re.sub('@strong_tag@[\W]*@br@@br@\W*@end_strong_tag@', '', content, re.I | re.M | re.U | re.DOTALL)
        
        # loai bo br trong the strong
        content = re.sub(r'@strong_tag@[\r\n\s]*(@br@)*([^@br@].*?)[\r\n\s]*(@br@)*[\r\n\s]*@end_strong_tag@', r'@strong_tag@\2@end_strong_tag@', content, 0, re.I | re.M | re.DOTALL)
        content = re.sub(r'@strong_tag@(.*?)(@br@)*[\r\n\s]*@end_strong_tag@', r'@strong_tag@\1@end_strong_tag@', content, 0, re.I | re.M | re.DOTALL)
        
        # loai bo the strong rong~
        content = re.sub('@strong_tag@\s*@end_strong_tag@', '', content, re.I | re.M | re.U | re.DOTALL)
        
        # Loai bo 2 @br@ dau tien
        content = content.strip()
        if content.startswith('@br@@br@') :
            content = content[8:]
        
        # Loai bo 2 @br@ cuoi cung
        content = content.strip()
        if content.endswith('@br@@br@') :
            content = content[:-8]
                
        #content = content.replace('@br@@br@', '\r\n@br@@br@\r\n')
        content = content.strip()
        
        # Replace multi @br@@br@ --> 1 @br@@br@
        content = re.sub(u'@br@@br@(\r\n)*(\u00a0)*\s*(\r\n)*@br@@br@', '@br@@br@', content, 0, re.DOTALL | re.U | re.M)

        #neu start la @br@@br@ --> replace
        if content.startswith("@br@@br@"):
            content = content[8:]
        
        # Replace
        content = content.replace('@br@', '<br/>')
        content = content.replace('@img@', '<img')
        content = content.replace('@end_img@', '/>')
        #content = content.replace('@br@', '<br/>\r\n')       
        content = content.replace('@strong_tag@', '<strong>')
        content = content.replace('@end_strong_tag@', '</strong>')
        content = content.replace('@p_tag@', '<p>')
        content = content.replace('@end_p_tag@', '</p>')
        content = content.replace('@em_tag@', '<em>')
        content = content.replace('@end_em_tag@', '</em>')  
        
        #print content
        return content
