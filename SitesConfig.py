# -*- coding: utf8 -*-

'''
1 - Nông nghiệp
2 - Kiến trúc & xây dựng
3 - Kinh tế & tài chính
4 - Môi trường
5 - Pháp luật & an ninh
6 - Đời sống & nghệ thuật & giải trí
7 - Tình yêu & hôn nhân
8 - Y học & sức khỏe
9 - Chính trị & quân sự
10- Khoa học
11- Xã hội & văn hóa & giáo dục
12- Thể thao
13- Công nghệ
14- Phương tiện (ô tô & xe máy)
'''
SITES = [
	{
		'vnexpress.net' : [
			# 1 - Nông nghiệp
			{'cate_id' : 1, 'class' : '', 'url': '' }

			# 2 - Kiến trúc & xây dựng
			

			# 3 - Kinh tế & tài chính
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/chung-khoan/', }
			#,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/chung-khoan/page/${1-10}.html', }
			
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/tien-cua-toi/page/${1-10}.html'}
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/bat-dong-san/'}
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/hang-hoa/'}
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/'}
			,{'cate_id' : 3, 'class' : 'vnexpress_net', 'url': 'http://kinhdoanh.vnexpress.net/tin-tuc/quoc-te/'}

			# 4 - Môi trường
			
			# 5 - Pháp luật & an ninh
			,{'cate_id' : 5, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/phap-luat/ho-so-pha-an'}
			,{'cate_id' : 5, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/phap-luat/tu-van'}
			,{'cate_id' : 5, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/phap-luat/'}			

			# 6 - Đời sống & nghệ thuật & giải trí

			
			# 7 - Tình yêu & hôn nhân

			
			# 8 - Y học & sức khỏe
			
			# 9 - Chính trị & quân sự
			
			# 10- Khoa học
			
			# 11- Xã hội & văn hóa & giáo dục
			,{'cate_id' : 11, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/giao-duc'}
			,{'cate_id' : 11, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/giao-duc/tuyen-sinh'}
			,{'cate_id' : 11, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/giao-duc/du-hoc'}
			,{'cate_id' : 11, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/giao-duc/tu-van'}
			,{'cate_id' : 11, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/giao-duc/nghe-trong-the-ky-21'}
			
			
			# 12- Thể thao
			
			# 13- Công nghệ
			,{'cate_id' : 14, 'class' : '', 'url': ''}
			
			# 14- Phương tiện (ô tô & xe máy)
			,{'cate_id' : 14, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/oto-xe-may/tu-van'}
			,{'cate_id' : 14, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/oto-xe-may/thi-truong'}
			,{'cate_id' : 14, 'class' : 'vnexpress_net', 'url': 'http://vnexpress.net/tin-tuc/oto-xe-may'}
			
		] 
	},{
		'dantri.com.vn' : [
			# 1. nong nghiep
			{'cate_id' : 1, 'class' : 'dantri_com_vn', 'url': ''}

			# 2. kien truc - xay dung 
			
			# 3 - Kinh tế & tài chính
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/thi-truong/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/tai-chinh-dau-tu/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/doanh-nghiep/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/bao-ve-ntd/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/quoc-te/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/nha-dat/trang-1.htm'}
			,{'cate_id' : 3, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/kinh-doanh/gia-ca/trang-1.htm'}

			# 4 - Môi trường
			,{'cate_id' : 4, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/xa-hoi/moi-truong/trang-1.htm'}
			
			# 5 - Pháp luật & an ninh
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': ''}
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': ''}
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': ''}

			# 6 - Đời sống & nghệ thuật & giải trí
			
			# 7 - Tình yêu & hôn nhân
			
			# 8 - Y học & sức khỏe
			
			# 9 - Chính trị & quân sự
			
			# 10- Khoa học
			
			# 11- Xã hội & văn hóa & giáo dục
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/xa-hoi.htm'}
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/xa-hoi/doi-song/trang-1.htm'}
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/xa-hoi/phong-suky-su/trang-1.htm'}
			
			
			# 12- Thể thao
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/the-thao.htm'}
			,{'cate_id' : 5, 'class' : 'dantri_com_vn', 'url': 'http://dantri.com.vn/the-thao/the-thao-trong-nuoc/trang-1.htm'}			
			,{'cate_id' : 5, 'class' : 'dantri_com_vn',	'url' : 'http://dantri.com.vn/the-thao/the-thao-quoc-te/trang-1.htm'}		
			
			
			
			# 13- Công nghệ
			
			# 14- Phương tiện (ô tô & xe máy)
		] 
	}
]

if __name__ == '__main__':
	print 'Test parsing config: '
	for site in SITES:
		for siteName in site:
			print '==========================='
			print siteName
			print '==========================='
			for cate in site[siteName]:
				print cate['cate_id']
				print cate['url']
				print '------------'
	print 'DONE'