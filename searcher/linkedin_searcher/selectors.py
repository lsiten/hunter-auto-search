# 领英页面元素选择器定义

# ==================== 登录相关 ====================
LOGIN_URL = "https://www.linkedin.com/login"
HOME_URL = "https://www.linkedin.com"

# 登录页元素
LOGIN_USERNAME_INPUT = '#username, input[name="session_key"]'
LOGIN_PASSWORD_INPUT = '#password, input[name="session_password"]'
LOGIN_SUBMIT_BTN = 'button[type="submit"], .btn__primary--large'

# 登录状态检查
USER_AVATAR = ".global-nav__me-photo, .profile-photo"
USER_NAME = ".profile-name, .nav-item__name"

# ==================== 搜索相关 ====================
SEARCH_URL = "https://www.linkedin.com/search/results/people/"

# 搜索框
SEARCH_INPUT = '.search-global-typeahead__input, #global-nav-typeahead input'
SEARCH_BTN = '.search-global-typeahead__submit, .search-btn'

# 高级筛选
FILTER_LOCATION = ".location-filter, .geo-filter"
FILTER_CURRENT_COMPANY = ".current-company-filter"
FILTER_PAST_COMPANY = ".past-company-filter"
FILTER_INDUSTRY = ".industry-filter"
FILTER_SCHOOL = ".school-filter"
FILTER_PROFILE_LANGUAGE = ".language-filter"

# 连接度筛选
FILTER_NETWORK = ".network-filter"
NETWORK_FIRST = ".first-degree"
NETWORK_SECOND = ".second-degree"
NETWORK_THIRD = ".third-degree"

# ==================== 搜索结果列表 ====================
RESULT_LIST_CONTAINER = ".search-results__list, .reusable-search__entity-result-list"

# 单个搜索结果项
CANDIDATE_CARD_ITEM = ".entity-result, .search-result__item, .reusable-search__result-container"

# 候选人卡片元素
CANDIDATE_AVATAR = ".entity-result__universal-image img, .presence-entity__image"
CANDIDATE_NAME = ".entity-result__title-text, .actor-name"
CANDIDATE_TITLE = ".entity-result__primary-subtitle, .search-result__snippets"
CANDIDATE_LOCATION = ".entity-result__secondary-subtitle, .search-result__location"
CANDIDATE_CURRENT_COMPANY = ".entity-result__summary, .search-result__job-title"

# 连接按钮
BTN_CONNECT = ".entity-result__actions button, .search-result__actions button"
BTN_MESSAGE = ".message-anywhere-button"

# ==================== 个人详情页 ====================
PROFILE_URL_PATTERN = r"linkedin\.com/in/[^/]+"

# 基本信息
CANDIDATE_DETAIL_NAME = "h1.text-heading-xlarge, .pv-top-card--list li:first-child"
CANDIDATE_DETAIL_TITLE = ".text-body-medium.break-words, .pv-top-card--list li:nth-child(2)"
CANDIDATE_DETAIL_LOCATION = ".text-body-small.inline.t-black--light.break-words, .pv-top-card--list-bullet li:first-child"
CANDIDATE_DETAIL_AVATAR = ".pv-top-card__photo img, .presence-entity__image"

# 联系方式区域
CONTACT_SECTION = ".pv-contact-info"
CONTACT_LINK = "#top-card-text-details-contact-info, .pv-top-card--contact-see-more"
CONTACT_EMAIL = ".pv-contact-info__contact-type.ci-email a"
CONTACT_PHONE = ".pv-contact-info__contact-type.ci-phone span"
CONTACT_WEBSITE = ".pv-contact-info__contact-type.ci-websites a"
CONTACT_WECHAT = ".pv-contact-info__contact-type.ci-wechat"

# 关于部分
ABOUT_SECTION = ".pv-about-section, .summary"
ABOUT_CONTENT = ".pv-about__summary-text, .summary__text"

# 工作经历
EXPERIENCE_SECTION = ".experience-section, #experience-section"
EXPERIENCE_ITEM = ".pv-entity__position-group-pager, .experience-item"
EXPERIENCE_COMPANY = ".pv-entity__secondary-title, .company-name"
EXPERIENCE_POSITION = ".t-16.t-black.t-bold, .position-title"
EXPERIENCE_DURATION = ".pv-entity__date-range span:nth-child(2), .date-range"
EXPERIENCE_LOCATION = ".pv-entity__location span:nth-child(2), .location"
EXPERIENCE_DESCRIPTION = ".pv-entity__description, .description"

# 教育经历
EDUCATION_SECTION = ".education-section, #education-section"
EDUCATION_ITEM = ".pv-education-entity, .education-item"
EDUCATION_SCHOOL = ".pv-entity__school-name, .school-name"
EDUCATION_DEGREE = ".pv-entity__degree-name span:nth-child(2), .degree"
EDUCATION_MAJOR = ".pv-entity__fos span:nth-child(2), .field-of-study"
EDUCATION_DURATION = ".pv-entity__dates span:nth-child(2), .date-range"

# 技能
SKILLS_SECTION = ".pv-skill-categories-section, .skills-section"
SKILL_ITEM = ".pv-skill-category-entity__name-text, .skill-item"

# 证书
CERTIFICATIONS_SECTION = ".certifications-section"

# 项目
PROJECTS_SECTION = ".projects-section"

# ==================== 分页相关 ====================
PAGINATION = ".artdeco-pagination, .search-results__pagination"
NEXT_PAGE_BTN = ".artdeco-pagination__button--next, .next"
PAGE_ITEMS = ".artdeco-pagination__indicator"
CURRENT_PAGE = ".artdeco-pagination__indicator--active"

# 无限加载 (领英使用滚动加载)
INFINITE_SCROLL_TRIGGER = ".infinite-scroll__trigger"

# ==================== 消息相关 ====================
MESSAGE_MODAL = ".msg-overlay-conversation-bubble"
MESSAGE_INPUT = ".msg-form__contenteditable"
MESSAGE_SEND_BTN = ".msg-form__send-button"

# ==================== 反爬/验证元素 ====================
CHALLENGE_PAGE = ".challenge-form, .login-challenge"
CAPTCHA_IMAGE = ".captcha-image, #captcha-internal"
CAPTCHA_INPUT = 'input[name="captcha"]'
VERIFY_EMAIL_INPUT = 'input[name="pin"]'

# ==================== URL 模式 ====================
URL_PATTERNS = {
    'login': r'linkedin\.com/login',
    'search': r'linkedin\.com/search/results/people',
    'profile': r'linkedin\.com/in/[^/]+',
    'messaging': r'linkedin\.com/messaging',
}

# ==================== API 端点 (谨慎使用) ====================
API_ENDPOINTS = {
    'search': '/voyager/api/search/cluster',
    'profile': '/voyager/api/identity/profiles',
    'message': '/voyager/api/messaging/conversations',
}
