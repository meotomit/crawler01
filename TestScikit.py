# -*- coding: utf-8 -*-

'''
Created on Dec 28, 2014

@author: phuckx
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer

import numpy as np
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem

def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold croos validation iterator of k=5 folds
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(
        np.mean(scores), sem(scores))

def get_stop_words():
    stop_words = set(['all', 'six', 'less', 'being', 'indeed', 'over', 'move', 'anyway', 'four', 'not', 'own', 'through', 'yourselves', 'fify', 'where', 'mill', 'only', 'find', 'before', 'one', 'whose', 'system', 'how', 'somewhere', 'with', 'thick', 'show', 'had', 'enough', 'should', 'to', 'must', 'whom', 'seeming', 'under', 'ours', 'has', 'might', 'thereafter', 'latterly', 'do', 'them', 'his', 'around', 'than', 'get', 'very', 'de', 'none', 'cannot', 'every', 'whether', 'they', 'front', 'during', 'thus', 'now', 'him', 'nor', 'name', 'several', 'hereafter', 'always', 'who', 'cry', 'whither', 'this', 'someone', 'either', 'each', 'become', 'thereupon', 'sometime', 'side', 'two', 'therein', 'twelve', 'because', 'often', 'ten', 'our', 'eg', 'some', 'back', 'up', 'go', 'namely', 'towards', 'are', 'further', 'beyond', 'ourselves', 'yet', 'out', 'even', 'will', 'what', 'still', 'for', 'bottom', 'mine', 'since', 'please', 'forty', 'per', 'its', 'everything', 'behind', 'un', 'above', 'between', 'it', 'neither', 'seemed', 'ever', 'across', 'she', 'somehow', 'be', 'we', 'full', 'never', 'sixty', 'however', 'here', 'otherwise', 'were', 'whereupon', 'nowhere', 'although', 'found', 'alone', 're', 'along', 'fifteen', 'by', 'both', 'about', 'last', 'would', 'anything', 'via', 'many', 'could', 'thence', 'put', 'against', 'keep', 'etc', 'amount', 'became', 'ltd', 'hence', 'onto', 'or', 'con', 'among', 'already', 'co', 'afterwards', 'formerly', 'within', 'seems', 'into', 'others', 'while', 'whatever', 'except', 'down', 'hers', 'everyone', 'done', 'least', 'another', 'whoever', 'moreover', 'couldnt', 'throughout', 'anyhow', 'yourself', 'three', 'from', 'her', 'few', 'together', 'top', 'there', 'due', 'been', 'next', 'anyone', 'eleven', 'much', 'call', 'therefore', 'interest', 'then', 'thru', 'themselves', 'hundred', 'was', 'sincere', 'empty', 'more', 'himself', 'elsewhere', 'mostly', 'on', 'fire', 'am', 'becoming', 'hereby', 'amongst', 'else', 'part', 'everywhere', 'too', 'herself', 'former', 'those', 'he', 'me', 'myself', 'made', 'twenty', 'these', 'bill', 'cant', 'us', 'until', 'besides', 'nevertheless', 'below', 'anywhere', 'nine', 'can', 'of', 'your', 'toward', 'my', 'something', 'and', 'whereafter', 'whenever', 'give', 'almost', 'wherever', 'is', 'describe', 'beforehand', 'herein', 'an', 'as', 'itself', 'at', 'have', 'in', 'seem', 'whence', 'ie', 'any', 'fill', 'again', 'hasnt', 'inc', 'thereby', 'thin', 'no', 'perhaps', 'latter', 'meanwhile', 'when', 'detail', 'same', 'wherein', 'beside', 'also', 'that', 'other', 'take', 'which', 'becomes', 'you', 'if', 'nobody', 'see', 'though', 'may', 'after', 'upon', 'most', 'hereupon', 'eight', 'but', 'serious', 'nothing', 'such', 'why', 'a', 'off', 'whereby', 'third', 'i', 'whole', 'noone', 'sometimes', 'well', 'amoungst', 'yours', 'their', 'rather', 'without', 'so', 'five', 'the', 'first', 'whereas', 'once'])
    return stop_words

if __name__ == '__main__':
    from sklearn.datasets import fetch_20newsgroups
    news = fetch_20newsgroups(subset='all')
    print type(news.data), type(news.target), type(news.target_names)
    print news.target_names
    print len(news.data)
    print len(news.target)
    print news.data[0]
    print news.target[0], news.target_names[news.target[0]]
    
    '''
    clf_1 = Pipeline([
        ('vect', CountVectorizer()),
        ('clf', MultinomialNB()),
    ])
    clf_2 = Pipeline([
        ('vect', HashingVectorizer(non_negative=True)),
        ('clf', MultinomialNB()),
    ])
    clf_3 = Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', MultinomialNB()),
    ])
    
    clfs = [clf_1, clf_2, clf_3]
    for clf in clfs:
        evaluate_cross_validation(clf, news.data, news.target, 5)
    '''
    stop_words = get_stop_words()
    '''
    clf_7 = Pipeline([
        ('vect', TfidfVectorizer(
                    stop_words=stop_words,
                    token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",         
        )),
        ('clf', MultinomialNB(alpha=0.01)),
    ]) 
    
    evaluate_cross_validation(clf_7, news.data, news.target, 5)
    '''
    
    
    
    from sklearn.feature_extraction.text import TfidfTransformer
    transformer = TfidfTransformer()
    
    def my_tokenizer(s):
        return s.split()
    vectorizer = CountVectorizer(tokenizer=my_tokenizer)
    str = 'I am sure some bashers of Pens fans are pretty confused about the lack'
    print vectorizer.build_analyzer()(str)
    print vectorizer.build_tokenizer()(str)
    print vectorizer.build_preprocessor()(str)
    
    s1 = 'rạng sáng nay theo giờ hà_nội danh_hiệu cầu_thủ giá_trị mvp giải mls năm được công_bố tiền_đạo gốc việt_lee_nguyễn ứng_viên sáng_giá không kém đôi ngôi_sao đá giải ngoại_hạng robbie_keane los_angeles_galaxy obafemi_martins seattle_sounders bình_chọn dựa số phiếu clb dự mls giới truyền_thông cầu_thủ robbie_keane người số phiếu trận chung_kết mls cup robbie_keane los_angeles_galaxy giành danh_hiệu cầu_thủ giá_trị mls lee_nguyễn được đánh_giá cao bình_chọn ảnh espn lee_nguyễn xếp thứ_ba bình_chọn đạt tổng_số phiếu mùa lee_nguyễn ghi bàn năm pha kiến_tạo cuối giải thi_đấu ấn_tượng vai_trò cầm_trịch lối chơi ghi_bàn cho new_england_revolution vòng play off mls cup tiền vệ_sinh năm ghi thêm hai bàn ba pha kiến_tạo đưa revolution đoạt vô_địch mls khu_vực miền đông giành vé dự chung_kết mls cup đối_đầu đội bóng keane la galaxy tháng lee_nguyễn được hlv jurgen_klinsmann triệu_tập trở_lại tuyển mỹ nhờ phong_độ ấn_tượng mls cựu inter_milan newcastle_utd obafemi_martins đứng thứ_hai số phiếu bầu cầu_thủ clb phiếu bầu clb phiếu bầu truyền thông phiếu bầu cầu thủ tổng robbie_keane la galaxy obafemi_martins seattle_sounders lee_nguyễn new england rev bradley_wright phillips ny  red_bulls tuấn'
    s2 = 'lee_nguyễn trải một năm thi_đấu hoàn_hảo ảnh usa today kết_quả được công_bố trang thông_tin chính_thức ban tổ_chức giải mls phần bình_luận tiền_vệ công lee_nguyễn đoạn lọt danh_sách bầu_chọn cuối_cùng cho danh_hiệu cầu_thủ giá_trị mls cho thấy lee_nguyễn một bước đột_phá sự_nghiệp nơi đanh ghi bàn đứng thứ_tư danh_sách vua_phá_lưới mùa vừa_qua tiền_vệ ghi_bàn cao lịch_sử mls chân chuyền đứng thứ_hai new_england năm pha kiến_tạo thành_công lee_nguyễn hoàn_toàn xứng_đáng lần đầu_tiên được lọt vào đội_hình tiêu_biểu mùa pha lập_công kiến_tạo lối chơi sáng_tạo ổn_định lee_nguyễn góp_phần quan_trọng làm_nên mùa giải thành_công rực_rỡ new_england_revolution họ nhì mls miền đông khi đăng_quang mls cup khu_vực đồng_nghĩa một suất vào chung_kết mls cup toàn_quốc nhờ lọt vào danh_sách rút_gọn cuối_cùng cho đua cầu_thủ giá_trị mvp robbie_keane los_angeles_galaxy obafemi_martins seattle_sounders bàn thắng gỡ hòa 1-1 vào lưới houston_dynamo tuần ngôi_sao sinh năm lọt danh_sách bốn bàn thắng đẹp mls sau bảy năm được gọi trở_lại đội_tuyển mỹ đội_hình tiêu_biểu mùa vừa_qua los_angles_galaxy đóng_góp nhiều ba cá_nhân chia đều hàng thủ đến hàng công đội bóng đối_thủ cạnh_tranh vô_địch mls cup lee_nguyễn revolution sân stubhub_center california ngày tới đội_hình tiêu_biểu mls mùa thủ_môn bill_hamid dc united hậu_vệ bobby_boswell dc united omar_gonzalez los_angeles_galaxy chad_marshall seattle_sounders tiền_vệ landon_donovan los_angeles_galaxy thierry_henry new_york_red_bulls lee_nguyễn new_england_revolution diego_valeri portland_timbers tiền_đạo robbie_keane los_angeles_galaxy obafemi_martins seattle_sounders fc bradley_wright phillips new_york_red_bulls đông_anh'
    s3 = 'thành_lương đỏ làm_nên tuyệt_phẩm trận đấu cuối_cùng bảng philippines ảnh giang_huy malaysia tập_trung hôm_qua để chuẩn_bị cho trận đấu tuyển việt_nam ngày sân_nhà shah_alam sau khi lách khe cửa hẹp để giành vị_trí thứ_hai bảng tay đội singapore thầy_trò salleh háo_hức muốn được kết_quả thật tốt một lời xin_lỗi để cđv nhà thất_vọng thời_gian gì phát_biểu có_thể thấy salleh nghiên_cứu kỹ báo_cáo hlv_u2 ong_kim_swee người được liên_đoàn bóng_đá malaysia fam cử sang hà_nội theo_dõi đối_thủ bảng trọng_tâm tuyển việt_nam đá giao_hữu tuyển việt_nam giải đấu nên phần_nào biết làm gì để kiềm_chế sức_mạnh họ salleh tiết_lộ báo_giới malaysia chúng tô đặc_biệt cẩn_trọng số nguyễn_văn_quyết số phạm_thành_lương cầu_thủ nguy_hiểm ong_kim_swee cho biết như_thế cầu_thủ văn_quyết đỏ chưa ghi_bàn được đối_thủ đánh_giá cao lối chơi ảnh giang_huy cá_nhân ong_kim_swee đưa nhận_xét tuyển việt_nam sau một thời_gian do_thám đội bóng xây_dựng được một phong_cách hoàn_toàn khác_biệt thời hlv người nhật_bản_toshiya_miura họ cầm bóng tốt không_bao_giờ chuyền bóng ngược sau luôn hướng lên phía miura sở_hữu cầu_thủ kỹ_thuật cá_nhân tốt malaysia cảnh_giác mỗi khi đối_phương bóng sát vòng cấm_địa việt_nam ghi hai bàn vào lưới philippines cú sút xa khi được hỏi điểm yếu tuyển việt_nam ong_kim_swee người giúp u23 malaysia vô_địch sea games tỏ bí_hiểm gì thấy một tập_thể gắn_kết mỗi vị_trí đều điểm yếu họ để thủng lưới ba lần điểm yếu có_thể tận_dụng khai_thác hlv salleh đen âm_thầm chuẩn_bị kế_hoạch gây bất_ngờ tuyển việt_nam sân_nhà ảnh ts bên_cạnh việc tìm cách phong_tỏa hai ngòi_nổ tuyển việt_nam salleh cố_gắng giải_quyết khoảng_trống shukor_adan mohd_amri_yahya để hai cầu_thủ trụ_cột đều vắng_mặt trận lượt_đi án treo_giò indra_putra_mahyuddin kunanlan manaf_mamat đều có_thể được tung vào sân_sau khi minh_chứng được khả_năng buổi tập safiq_rahim mohd_muslim có_thể đá vị_trí tiền_vệ trụ thay_thế cho shukor_adan salleh tiết_lộ ít_nhiều khung đội_hình thi_đấu cuối tuần người thay_thế amri_yahya trận đấu kulanan hoặc manaf_mamat tuấn'
    corpus = [s1, s2, s3]
    
    
    print 'DOne'