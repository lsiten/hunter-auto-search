# 猎聘页面元素选择器定义

# ==================== 登录相关 ====================
LOGIN_URL = "https://www.liepin.com/"
HOME_URL = "https://www.liepin.com"

# 登录页元素
LOGIN_LINK = ".login-btn, [data-selector='login']"
LOGIN_QRCODE = ".qrcode-img, .qr-code img"
LOGIN_QRCODE_REFRESH = ".refresh-qrcode"
LOGIN_TAB_USERNAME = ".tab-account"
LOGIN_USERNAME_INPUT = 'input[name="username"], #login'
LOGIN_PASSWORD_INPUT = 'input[name="password"], #password'
LOGIN_SUBMIT_BTN = ".submit-btn, .btn-login"

# 登录状态检查
USER_AVATAR = ".user-avatar, .avatar img"
USER_NAME = ".user-name, .username"

# ==================== 搜索相关 (招聘方后台) ====================
SEARCH_URL = "https://hunter.liepin.com/resume/search"

# 搜索框
SEARCH_KEYWORD_INPUT = '.search-input, [data-selector="keyword"]'
SEARCH_BTN = '.search-btn, .btn-search'

# 高级筛选
FILTER_CITY = ".city-filter, .area-selector"
FILTER_SALARY = ".salary-filter, .expectSalary-selector"
FILTER_EXPERIENCE = ".experience-filter, .workYears-selector"
FILTER_EDUCATION = ".education-filter, .eduLevel-selector"
FILTER_POSITION = ".position-filter"
FILTER_COMPANY = ".company-filter"

# ==================== 搜索结果列表 ====================
RESULT_LIST_CONTAINER = ".resume-list, .search-result-list"

# 单个候选人卡片
CANDIDATE_CARD_ITEM = ".resume-card, .search-item"

# 候选人卡片元素
CANDIDATE_AVATAR = ".avatar img, .head-img"
CANDIDATE_NAME = ".name, .user-name, .resume-name"
CANDIDATE_TITLE = ".title, .job-title, .position"
CANDIDATE_CURRENT_COMPANY = ".current-company, .latest-company"
CANDIDATE_EXPECTED_SALARY = ".expected-salary, .salary-expect"
CANDIDATE_LOCATION = ".location, .work-city"
CANDIDATE_WORK_YEARS = ".work-years, .experience"
CANDIDATE_DEGREE = ".degree, .edu-level"
CANDIDATE_AGE = ".age"
CANDIDATE_LAST_ACTIVE = ".last-active, .active-time"

# 查看联系方式按钮
BTN_VIEW_CONTACT = ".view-contact-btn, .get-contact"

# ==================== 详情页元素 ====================
CANDIDATE_DETAIL_NAME = ".name, .resume-name"
CANDIDATE_DETAIL_AVATAR = ".avatar img"
CANDIDATE_DETAIL_TITLE = ".current-position, .job-title"
CANDIDATE_DETAIL_CURRENT_COMPANY = ".current-company"
CANDIDATE_DETAIL_EXPECTED_SALARY = ".expected-salary, .salary"
CANDIDATE_DETAIL_LOCATION = ".location, .city"
CANDIDATE_DETAIL_AGE = ".age"
CANDIDATE_DETAIL_GENDER = ".gender"
CANDIDATE_DETAIL_PHONE = ".phone, .mobile"
CANDIDATE_DETAIL_EMAIL = ".email"
CANDIDATE_DETAIL_WECHAT = ".wechat"

# 工作经历
EXPERIENCE_SECTION = ".work-experience, .work-list, .experience-section"
EXPERIENCE_ITEM = ".work-item, .exp-item"
EXPERIENCE_COMPANY = ".company-name, .corp-name"
EXPERIENCE_POSITION = ".position, .title"
EXPERIENCE_DURATION = ".duration, .date-range, .time"
EXPERIENCE_DESCRIPTION = ".description, .job-content, .desc"

# 教育经历
EDUCATION_SECTION = ".education-experience, .edu-list, .education-section"
EDUCATION_ITEM = ".edu-item, .education-item"
EDUCATION_SCHOOL = ".school-name, .school"
EDUCATION_DEGREE = ".degree, .education"
EDUCATION_MAJOR = ".major, .specialty"
EDUCATION_DURATION = ".duration, .date-range"

# 技能标签
SKILL_TAGS = ".skill-tags .tag, .skills .skill-item, .ability-item"

# 项目经历
PROJECT_SECTION = ".project-experience, .project-list"
PROJECT_ITEM = ".project-item"

# ==================== 分页相关 ====================
PAGINATION = ".pagination, .pager"
NEXT_PAGE_BTN = ".next-page, .next, .pagination .next"
PREV_PAGE_BTN = ".prev-page, .prev"
PAGE_ITEMS = ".pagination .page-item, .pager .num"
CURRENT_PAGE = ".pagination .active, .current"

# ==================== 错误/提示元素 ====================
ERROR_MESSAGE = ".error-message, .error-tip, .message"
VERIFY_SLIDER = ".slider-btn, .slide-verify"
VERIFY_CAPTCHA = '.geetest_item_img, .captcha-img'

# ==================== URL 模式 ====================
URL_PATTERNS = {
    'login': r'liepin\.com/?$',
    'hunter_home': r'hunter\.liepin\.com',
    'search': r'hunter\.liepin\.com/resume/search',
    'candidate_detail': r'hunter\.liepin\.com/resume/detail',
    'resume_view': r'hunter\.liepin\.com/resume/view',
}

# ==================== API 端点 ====================
API_ENDPOINTS = {
    'search': '/hunter/resume/api/search',
    'resume_detail': '/hunter/resume/api/detail',
    'contact': '/hunter/resume/api/contact',
}
