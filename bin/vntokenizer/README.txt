VN_TOKENIZER
================================================
I) TỔNG QUAN
-------------

	+) Chương trình vnTokenizer được sử dụng để tách từ các văn bản tiếng Việt (mã hóa bằng bảng mã Unicode UTF-8).
	
	+) Chương trình chạy dưới dạng dòng lệnh:
	 
		- vnTokenizer.sh nếu chạy trên các hệ điều hành Linux/Unix/Mac OS
		- vnTokenizer.bat nếu chạy trên các hệ điều hành MS Windows
		
	+) Yêu cầu: Máy cần cài JRE (Java Runtime Environment) phiên bản 1.6. JRE có thể tải về từ địa chỉ  website 
			Java của Sun Microsystems: http://java.sun.com/
	
II) DỮ LIỆU
------------

	Trong một lần chạy vnTokenizer có thể tách từ một tệp hoặc đồng thời nhiều tệp nằm trong cùng một thư mục. 
	
	1) Tách từ một tệp:
	
		+) Dữ liệu cần cung cấp cho chương trình gồm 1 tệp văn bản tiếng Việt, dạng thô (ví dụ như tệp README.txt này).
			  
		+) Kết quả: Một tệp văn bản kết quả tách từ được ghi dưới định dạng đơn giản hoặc định dạng XML, tùy 
			theo lựa chọn của người sử dụng (xem ví dụ dưới đây). 
				
			
	2) Tách từ nhiều tệp nằm trong một thư mục:
	
		+) Dữ liệu cần cung cấp gồm một thư mục chứa các tệp văn bản thô cần tách từ (thư mục input) và một thư mục trống 
			(thư mục output) để chứa kết quả tách từ.
		
		+) Mặc định, chương trình sẽ tự động quét toàn bộ thư mục input và lọc ra tất cả các tệp có đuôi là ".txt".  
			 Người sử dụng có thể thay đổi đuôi mặc định này thành đuôi bất kì, ví dụ ".seg" bằng tùy chọn -e của dòng lệnh 
			 (xem ví dụ dưới đây). 
			 
		+) Kết quả: Tập các tệp kết quả tách từ trong thư mục output, các tệp này có cùng tên với tệp input tương ứng, 
			tức là tệp input/abc.txt sẽ có kết quả là tệp output/abc.txt.  
		  
		
III) CHẠY CHƯƠNG TRÌNH
-----------------------
			
	1) Tách từ một tệp:
	
			vnTokenizer.sh -i <tệp-input> -o <tệp-output> [<các-tùy-chọn>]
		
			Hai tùy chọn -i và -o là bắt buộc. Ngoài ra, người dùng có thể cung cấp các tùy chọn không bắt buộc sau đây:
			
			+) -xo : dùng định dạng XML để biểu diễn kết quả thay vì định dạng mặc định là văn bản thô.
			  
			+) -nu : không sử dụng dấu gạch dưới (no underscore) khi ghi kết quả. Nếu tùy chọn này được sử dụng thì trong 
					kết quả, các âm tiết không được nối với nhau bằng ký tự gạch dưới, mà bằng ký tự trắng.
			
			+) -sd : sử dụng mô-đun tách câu trước khi thực hiện tách từ. Nếu tùy chọn này được sử dụng thì trước tiên 
					vnTokenizer thực hiện tách văn bản input thành một tập các câu, sau đó thực hiện tách từ từng câu một.
					Mặc định thì mô-đun tách câu không được sử dụng, vnTokenizer thực hiện tách từ trên toàn bộ văn bản.

			Các tùy chọn này có thể được phối hợp đồng thời với nhau để cho ra kết quả mong muốn. 
		
		Ví dụ: 
		
			a) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.txt
				
				Tách từ tệp samples/test0.txt và ghi kết quả vào tệp samples/test0.tok.txt
				
			b) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.xml -xo
				
				Tương tự như a), tuy nhiên tệp kết quả samples/test0.tok.xml sẽ có định dạng XML.
				
			c) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.txt -sd 
				
				Tương tự như a) và sử dụng mô-đun tách câu trước khi tách từ.
	
	2) Tách từ một thư mục:
			
		Ngoài các tùy chọn như ở trên, khi tách từ thư mục, chương trình cung cấp thêm tùy chọn không bắt buộc
			  
				+) -e : chỉ định phần mở rộng của các tệp cần tách.
	 
	 	Ví dụ: 
	 	
	 		a) vnTokenizer.sh -i samples/input -o samples/output
	 		
	 			Thực hiện tách từ tất cả các tệp samples/input/*.txt, ghi kết quả ra thư mục samples/output. 
	 		
	 		b) vnTokenizer.sh -i samples/input -o samples/output -e .xyz
	 		 
	 		 	Thực hiện tách từ tất cả các tệp samples/input/*.xyz, ghi kết quả ra thư mục samples/output.
	 		 

VN_TAGGER
=================================================
(C) Le Hong Phuong, phuonglh@gmail.com,
	2008-2010,
	Hanoi University of Science,  
	Vietnam National University, Hanoi, Vietnam
==================================================

vnTagger version 4.2.0, released 04/2010.
==================================================

I. GENERAL INFORMATION

	vnTagger is a highly accurate tagger for Vietnamese texts. Its 
	precision and recall ratios are about 96% on a test set of the Vietnamese treebank. 
	It uses as additional libraries	vnTokenizer (a tokenizer for Vietnamese texts) 
	and Stanford Maxent Tagger v2.0.
	 
	These libraries are provided in the jars file of the lib directory. 
	
	The tagset in use contains 17 main lexical tags:
		
		1.  Np - Proper noun
		2.  Nc - Classifier
		3.  Nu - Unit noun
		4.  N - Common noun
		5.  V - Verb
		6.  A - Adjective
		7.  P - Pronoun
		8.  R - Adverb
		9.  L - Determiner
		10. M - Numeral
		11. E - Preposition
		12. C - Subordinating conjunction
		13. CC - Coordinating conjunction
		14. I - Interjection
		15. T - Auxiliary, modal words
		16. Y - Abbreviation
		17. Z - Bound morphemes
		18. X - Unknown
			
	There are also tags for delimiters and punctuations.
	
	
II. REQUIREMENT
 
	You need a JRE version 6.0 or above installed on your system. You may 
	download a JRE from the Java website of Sun Microsystems (http://java.sun.com/).
	
	
III. HOW TO RUN

	- On a Unix/Linux system, use the provided script "vnTagger.sh" 
		to run the program, on a MS Windows, use "vnTagger.bat".
	
	- This program is a core tagger for Vietnamese texts, it has no graphical
		 user interface (GUI).
		 
	- If you want to use a GUI version of the tagger, you should download vnToolkit, an 
		Eclipse Rich Client application. vnTagger, its GUI and other tools are bundled 
		as plug-ins of vnToolkit. NOTE: vnToolkit may NOT contain the latest version of vnTagger.
		  
	1) 	 How to tag a text file:
	----------------------------
		 You should provide two arguments for the program: an input text file to be tagged 
		 (with argument option -i) and an output file for the program to write result to 
		 (with argument option -o).
		 
		 For example:
		  
		  ./vnTagger.sh -i samples/0.txt  -o samples/0.tagged.xml
	 	
	 	Note that the file "0.txt" must exist and contain some Vietnamese text encoded in UTF-8
	 	encoding. The result file "0.tagged.xml" is a text file (A simple XML format) created by 
	 	the program and it is always encoded in UTF-8 encoding.
	 	
	 	By default, syllables of compound words are separated by spaces, you can use option -u
	 	to separate them by underscore (_) character. If you want that the result file is a plain 
	 	text instead of an XML file, use the option -p.  
	 	
	 	Thus, the command
	 	
	 		./vnTagger.sh -i samples/0.txt  -o samples/0.tagged.xml -u
	 		
	 	will produce output with syllables separated by underscore characters.
	 	
	 	The command 
	 	
	 		./vnTagger.sh -i samples/0.txt  -o samples/0.tagged.txt -u -p 
	 		
	 	will produce output with syllables separated by underscore characters and use a plain text
		output file instead of an XML file.
	 	
	- Under Microsoft Windows, use the provided script "vnTagger.bat" instead of "vnTagger.sh"  
		to run the program. All the options are similar as described above.

	2) 	 How to test a tagged file:
	-------------------------------
	
	- If you want to test the accuracy of the tagger on a correctly tagged file, use the argument 
		-t on the file to test, for example:
		
			./vnTagger.sh -t samples/1.tagged.txt
		
		Results of the test will be outputed to the standard console. Note that the test file 
		need to be a plain text file in which syllables are separated by underscores, words are 
		separated by spaces. 


IV. HOW TO USE THE API
	
	The main class of the tagger is vn.hus.nlp.tagger.VietnameseMaxentTagger. This class provides
	three methods to tag text 
		
		+ public String tagText(String text)
		
			Tag a text and return a tagged string.
			
		+ public void tagFile(String inputFile, String outputFile, IOutputer outputer)
		
			Tag an input text file and write the result to an output file, using an outputer.
			
		+ public void tagFile(String inputFile, String outputFile)
		
			Tag an input text file and write the result to an output file, using a default plain outputer.
			
	and a method for test a tagged file:
	
		+ public void testFile(String filename)
			
			Test a tagged file.
    			
V. LICENSE
  
  		See the LICENSE file.
  		
 VI. CONTACT
 
	The program and this short documentation for the tagger is written by Le Hong Phuong (phuonglh@gmail.com). 
	Any comments, questions and discussions will be appreciated.   
 	 
