# BOSS 直聘页面元素选择器定义

# ==================== 登录相关 ====================
LOGIN_URL = "https://www.zhipin.com/web/user/?ka=header-login"
HOME_URL = "https://www.zhipin.com"

# 登录页元素
LOGIN_QRCODE = ".qrcode-img"  # 二维码图片
LOGIN_QRCODE_REFRESH = ".refresh-btn"  # 刷新二维码按钮
LOGIN_TAB_PASSWORD = ".password-tab"  # 密码登录tab
LOGIN_USERNAME_INPUT = 'input[name="account"]'
LOGIN_PASSWORD_INPUT = 'input[name="password"]'
LOGIN_SUBMIT_BTN = ".btn-login"

# 登录状态检查
USER_AVATAR = ".user-avatar, .user-center-avatar"  # 用户头像(已登录标识)
USER_NAME = ".user-name, .username"  # 用户名

# ==================== 搜索相关 ====================
SEARCH_URL = "https://www.zhipin.com/web/geek/job"

# 搜索框
SEARCH_INPUT = '.search-input-box input[type="text"]'
SEARCH_BTN = '.search-btn, .btn-search'

# 高级筛选
FILTER_CITY = ".city-selector"
FILTER_SALARY = ".salary-selector"
FILTER_EXPERIENCE = ".experience-selector"
FILTER_EDUCATION = ".education-selector"

# ==================== 搜索结果列表 ====================
# 结果列表容器
RESULT_LIST_CONTAINER = ".job-list-box, .search-job-result"

# 单个职位卡片 (注意：BOSS 直聘现在是职位卡片，不是候选人卡片)
JOB_CARD_ITEM = ".job-card-wrapper, .job-list-item"

# 职位卡片内的元素
JOB_TITLE = ".job-name"  # 职位名称
JOB_SALARY = ".job-salary"  # 薪资
JOB_AREA = ".job-area"  # 工作地点
JOB_COMPANY = ".company-name"  # 公司名称
JOB_COMPANY_INFO = ".company-info"  # 公司信息(行业/融资/规模)
JOB_TAGS = ".job-card-footer .tag-list li"  # 职位标签
JOB_BTN = ".job-card-body"  # 点击进入详情

# 候选人/求职者相关 (如果有的话)
CANDIDATE_AVATAR = ".avatar, .head-portrait"
CANDIDATE_NAME = ".name, .user-name"
CANDIDATE_TITLE = ".title, .job-title"
CANDIDATE_EXPERIENCE = ".experience, .work-years"

# ==================== 详情页元素 ====================
# 候选人详情页
CANDIDATE_DETAIL_NAME = ".resume-name, .name"
CANDIDATE_DETAIL_AVATAR = ".resume-avatar img"
CANDIDATE_DETAIL_TITLE = ".current-position"
CANDIDATE_DETAIL_SALARY = ".expected-salary"
CANDIDATE_DETAIL_LOCATION = ".location"
CANDIDATE_DETAIL_AGE = ".age"
CANDIDATE_DETAIL_GENDER = ".gender"

# 工作经历
EXPERIENCE_SECTION = ".work-experience, .work-list"
EXPERIENCE_ITEM = ".work-item, .experience-item"
EXPERIENCE_COMPANY = ".company-name"
EXPERIENCE_POSITION = ".position-name"
EXPERIENCE_DURATION = ".duration, .time"
EXPERIENCE_DESCRIPTION = ".description, .job-content"

# 教育经历
EDUCATION_SECTION = ".education-experience, .edu-list"
EDUCATION_ITEM = ".edu-item"
EDUCATION_SCHOOL = ".school-name"
EDUCATION_DEGREE = ".degree"
EDUCATION_MAJOR = ".major"
EDUCATION_DURATION = ".duration"

# 技能标签
SKILL_TAGS = ".skill-tags .tag, .ability-item"

# 联系方式
CONTACT_PHONE = ".phone, .contact-phone"
CONTACT_EMAIL = ".email"
CONTACT_WECHAT = ".wechat"

# ==================== 分页相关 ====================
PAGINATION = ".pagination"
NEXT_PAGE_BTN = ".next-page, .pagination .next"
PAGE_ITEMS = ".pagination .page-item"
CURRENT_PAGE = ".pagination .active"

# ==================== 错误/提示元素 ====================
ERROR_MESSAGE = ".error-message, .tip-message"
VERIFY_SLIDER = ".slider-btn"  # 滑块验证码
VERIFY_CAPTCHA = '.geetest_item_img'  # 验证码图片

# ==================== URL 模式 ====================
URL_PATTERNS = {
    'login': r'/web/user/',
    'search': r'/web/geek/job',
    'job_detail': r'/job_detail/',
    'candidate_detail': r'/candidate/',
    'resume': r'/resume/',
}

# ==================== API 端点 (如果可以直接调用的话) ====================
API_ENDPOINTS = {
    'search': '/wapi/zpgeek/search/joblist.json',
    'job_detail': '/wapi/zpgeek/job/detail.json',
}
