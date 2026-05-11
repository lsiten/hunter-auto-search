# 脉脉页面元素选择器定义

# ==================== 登录相关 ====================
LOGIN_URL = "https://maimai.cn/login"
HOME_URL = "https://maimai.cn"

# 登录页元素
LOGIN_QRCODE_TAB = ".qr-login-tab, .tab-qrcode"
LOGIN_QRCODE = ".qrcode-img, .qr-code img"
LOGIN_QRCODE_REFRESH = ".refresh-qrcode, .btn-refresh"
LOGIN_TAB_PASSWORD = ".password-login-tab, .tab-account"
LOGIN_PHONE_INPUT = 'input[name="phone"], #phone'
LOGIN_CODE_INPUT = 'input[name="code"], #code'
LOGIN_GET_CODE_BTN = ".get-code-btn, .btn-send-code"
LOGIN_SUBMIT_BTN = ".submit-btn, .btn-login"

# 登录状态检查
USER_AVATAR = ".user-avatar, .avatar img, .header-avatar"
USER_NAME = ".user-name, .username, .header-name"

# ==================== 搜索相关 ====================
SEARCH_URL = "https://maimai.cn/search"

# 搜索框
SEARCH_INPUT = '.search-input, #searchInput, .header-search input'
SEARCH_BTN = '.search-btn, .btn-search, .header-search button'

# 高级筛选
FILTER_CITY = ".city-filter, .area-selector, .location-filter"
FILTER_COMPANY = ".company-filter, .corp-selector"
FILTER_POSITION = ".position-filter, .title-selector"
FILTER_INDUSTRY = ".industry-filter"
FILTER_SCHOOL = ".school-filter"

# 人脉深度筛选
FILTER_DEGREE = ".degree-filter"
DEGREE_1ST = ".degree-1, .first-degree"
DEGREE_2ND = ".degree-2, .second-degree"
DEGREE_3RD = ".degree-3, .third-degree"

# ==================== 搜索结果列表 ====================
RESULT_LIST_CONTAINER = ".search-result-list, .user-list, .contact-list"

# 单个用户卡片
CANDIDATE_CARD_ITEM = ".user-card, .search-item, .contact-item"

# 用户卡片元素
CANDIDATE_AVATAR = ".avatar img, .head-img, .user-avatar"
CANDIDATE_NAME = ".name, .user-name, .contact-name"
CANDIDATE_TITLE = ".title, .job-title, .position"
CANDIDATE_COMPANY = ".company, .corp-name, .current-company"
CANDIDATE_LOCATION = ".location, .city, .area"
CANDIDATE_DEGREE = ".degree, .connection-degree"
CANDIDATE_MUTUAL_CONTACTS = ".mutual-contacts, .common-friends"

# 操作按钮
BTN_ADD_CONTACT = ".add-contact-btn, .btn-add, .connect-btn"
BTN_SEND_MESSAGE = ".send-message-btn, .btn-message"
BTN_VIEW_PROFILE = ".view-profile, .card-click-area"

# ==================== 个人详情页 ====================
PROFILE_URL_PATTERN = r"maimai\.cn/web/personal"

# 基本信息
CANDIDATE_DETAIL_NAME = ".profile-name, .name, .user-name"
CANDIDATE_DETAIL_AVATAR = ".profile-avatar img, .avatar"
CANDIDATE_DETAIL_TITLE = ".profile-title, .job-title, .position"
CANDIDATE_DETAIL_COMPANY = ".profile-company, .current-company"
CANDIDATE_DETAIL_LOCATION = ".profile-location, .city, .location"
CANDIDATE_DETAIL_INDUSTRY = ".profile-industry, .industry"

# 详细信息区
PROFILE_INFO_SECTION = ".profile-info, .info-section"
INFO_ITEM = ".info-item, .detail-item"

# 标签
PROFILE_TAGS = ".profile-tags .tag, .user-tags .tag-item"

# 工作经历
EXPERIENCE_SECTION = ".work-experience, .experience-list, .work-list"
EXPERIENCE_ITEM = ".work-item, .experience-item"
EXPERIENCE_COMPANY = ".company-name, .corp-name, .employer"
EXPERIENCE_POSITION = ".position, .title, .job-title"
EXPERIENCE_DURATION = ".duration, .date-range, .time-period"
EXPERIENCE_DESCRIPTION = ".description, .job-content, .desc"

# 教育经历
EDUCATION_SECTION = ".education-experience, .edu-list, .education-list"
EDUCATION_ITEM = ".edu-item, .education-item"
EDUCATION_SCHOOL = ".school-name, .school"
EDUCATION_DEGREE = ".degree, .education"
EDUCATION_MAJOR = ".major, .specialty, .field"
EDUCATION_DURATION = ".duration, .date-range"

# 项目经历
PROJECT_SECTION = ".project-experience, .project-list"
PROJECT_ITEM = ".project-item"

# 技能标签
SKILL_TAGS = ".skill-tags .tag, .skills .skill-item, .ability-tags"

# 联系方式 (如果可见)
CONTACT_SECTION = ".contact-info, .contact-section"
CONTACT_PHONE = ".phone, .mobile, .telephone"
CONTACT_EMAIL = ".email, .mail"
CONTACT_WECHAT = ".wechat, .wx"

# ==================== 消息/聊天相关 ====================
MESSAGE_MODAL = ".chat-modal, .message-window"
MESSAGE_INPUT = ".message-input, .chat-input textarea"
MESSAGE_SEND_BTN = ".send-btn, .btn-send"

# 人脉关系
RELATION_PATH = ".relation-path, .connection-path"
MUTUAL_FRIENDS_LIST = ".mutual-friends-list, .common-contacts"

# ==================== 分页相关 ====================
PAGINATION = ".pagination, .pager"
NEXT_PAGE_BTN = ".next-page, .next, .pagination .next"
PAGE_ITEMS = ".pagination .page-item, .pager .num"
CURRENT_PAGE = ".pagination .active, .current-page"

# 无限加载
INFINITE_SCROLL_TRIGGER = ".load-more, .infinite-trigger"
LOAD_MORE_BTN = ".load-more-btn, .btn-load-more"

# ==================== 错误/提示/验证元素 ====================
ERROR_MESSAGE = ".error-message, .error-tip, .message-box"
VERIFY_SLIDER = ".slider-btn, .slide-verify, .captcha-slider"
VERIFY_CAPTCHA = '.captcha-img, .verify-img, .geetest_item_img'
VERIFY_CODE_INPUT = '.code-input, input[name="verifyCode"]'

# 会员/权限提示
MEMBER_LIMIT_TIP = ".member-limit, .vip-tip"
DAILY_LIMIT_TIP = ".daily-limit, .limit-tip"

# ==================== URL 模式 ====================
URL_PATTERNS = {
    'login': r'maimai\.cn/login',
    'home': r'maimai\.cn/?$',
    'search': r'maimai\.cn/search',
    'profile': r'maimai\.cn/web/personal',
    'message': r'maimai\.cn/web/im',
}

# ==================== API 端点 (谨慎使用) ====================
API_ENDPOINTS = {
    'search': '/api/search/user',
    'profile': '/api/user/profile',
    'contact': '/api/user/contact',
    'message': '/api/im/send',
}
