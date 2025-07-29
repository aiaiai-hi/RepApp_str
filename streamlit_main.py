import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Настройка страницы
st.set_page_config(
    page_title="Система отчетности - Корпоративный портал",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Загрузка кастомного CSS
def load_css():
    st.markdown("""
    <style>
    /* Корпоративные цвета */
    :root {
        --primary-color: #228B22;
        --secondary-color: #9ACD32;
        --accent-color: #FFD700;
        --background-color: #ffffff;
        --text-color: #2d3748;
        --muted-color: #718096;
        --border-color: #e2e8f0;
        --success-color: #228B22;
        --warning-color: #FFD700;
        --info-color: #9ACD32;
    }
    
    /* Основные стили */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Кастомные карточки */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        color: var(--text-color);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--muted-color);
        margin: 0;
    }
    
    .metric-change {
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }
    
    .metric-change.positive {
        color: var(--success-color);
    }
    
    .metric-change.negative {
        color: #e53e3e;
    }
    
    /* Таблица стилей */
    .dataframe {
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
    }
    
    .dataframe thead th {
        background-color: #f7fafc;
        color: var(--text-color);
        font-weight: 500;
        border-bottom: 1px solid var(--border-color);
        padding: 0.75rem;
    }
    
    .dataframe tbody td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Статус бейджи */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-registered {
        background-color: var(--primary-color);
        color: white;
    }
    
    .status-progress {
        background-color: var(--secondary-color);
        color: var(--text-color);
    }
    
    .status-waiting {
        background-color: var(--accent-color);
        color: var(--text-color);
    }
    
    .status-critical {
        background-color: #e53e3e;
        color: white;
    }
    
    /* Приоритет бейджи */
    .priority-high {
        background-color: #e53e3e;
        color: white;
    }
    
    .priority-medium {
        background-color: var(--secondary-color);
        color: var(--text-color);
    }
    
    .priority-low {
        background-color: var(--border-color);
        color: var(--text-color);
    }
    
    /* Боковая панель */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Кнопки */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #1e7e1e;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Селектбоксы */
    .stSelectbox > div > div {
        border-color: var(--border-color);
        border-radius: 0.375rem;
    }
    
    /* Заголовки секций */
    .section-header {
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin: 0;
    }
    
    .section-description {
        font-size: 0.875rem;
        color: var(--muted-color);
        margin: 0.25rem 0 0 0;
    }
    
    /* Логотип */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    .logo-dots {
        display: flex;
        gap: 0.25rem;
    }
    
    .logo-dot {
        width: 0.75rem;
        height: 2rem;
        border-radius: 0.125rem;
    }
    
    .logo-dot-1 { background-color: var(--accent-color); }
    .logo-dot-2 { background-color: var(--secondary-color); }
    .logo-dot-3 { background-color: var(--primary-color); }
    
    .logo-text h1 {
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-color);
    }
    
    .logo-text p {
        font-size: 0.75rem;
        color: var(--muted-color);
        margin: 0;
    }
    
    /* Информация в сайдбаре */
    .sidebar-info {
        margin-top: auto;
        padding-top: 2rem;
        border-top: 1px solid var(--border-color);
    }
    
    .sidebar-info p {
        font-size: 0.75rem;
        color: var(--muted-color);
        margin: 0.25rem 0;
    }
    
    /* Скрытие элементов Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tabs стилизация */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #f7fafc;
        border-radius: 0.75rem;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0.5rem;
        color: var(--muted-color);
        font-weight: 500;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: var(--text-color);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Данные для примера
@st.cache_data
def load_sample_data():
    # Генерируем данные для графиков
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн"]
    reports_data = [45, 52, 48, 61, 55, 67]
    
    # Данные по статусам
    status_data = {
        "Статус": ["Зарегистрированы", "В процессе", "Ожидают"],
        "Количество": [156, 89, 34],
        "Цвет": ["#228B22", "#9ACD32", "#FFD700"]
    }
    
    # Данные отчетов
    reports_df = pd.DataFrame({
        "ID": ["RPT-001", "RPT-002", "RPT-003", "RPT-004", "RPT-005"],
        "Название": [
            "Финансовый отчет Q2",
            "Отчет по продажам", 
            "HR отчет по персоналу",
            "Отчет по маркетингу",
            "Технический отчет"
        ],
        "Департамент": ["Финансы", "Продажи", "HR", "Маркетинг", "IT"],
        "Статус": ["Зарегистрирован", "В процессе", "Ожидает", "Зарегистрирован", "В процессе"],
        "Дата": ["2024-06-15", "2024-06-14", "2024-06-13", "2024-06-12", "2024-06-11"],
        "Приоритет": ["Высокий", "Средний", "Низкий", "Высокий", "Средний"]
    })
    
    return months, reports_data, status_data, reports_df

def render_sidebar():
    """Отрисовка боковой панели"""
    with st.sidebar:
        # Логотип
        st.markdown("""
        <div class="logo-container">
            <div class="logo-dots">
                <div class="logo-dot logo-dot-1"></div>
                <div class="logo-dot logo-dot-2"></div>
                <div class="logo-dot logo-dot-3"></div>
            </div>
            <div class="logo-text">
                <h1>Система отчетности</h1>
                <p>Корпоративный портал</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Основные разделы
        st.subheader("Основные разделы")
        
        # Навигация
        pages = {
            "📊 Дашборд": "dashboard",
            "📚 Обучение": "training", 
            "🔄 Этапы процесса": "process",
            "📤 Загрузка атрибутов": "upload",
            "❓ Часто задаваемые вопросы": "faq",
            "💬 Обратная связь": "feedback"
        }
        
        selected_page = st.radio("", list(pages.keys()), index=0)
        
        # Информация в нижней части
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-info">
            <p><strong>🏢 ООО "Компания"</strong></p>
            <p>Версия системы: 2.1.4</p>
            <p>Обновлено: 15.06.2024</p>
        </div>
        """, unsafe_allow_html=True)
        
        return pages[selected_page]

def render_metric_card(title, value, change=None, change_positive=True):
    """Отрисовка карточки метрики"""
    change_class = "positive" if change_positive else "negative"
    change_html = f'<p class="metric-change {change_class}">{change}</p>' if change else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">{title}</p>
        <p class="metric-value">{value}</p>
        {change_html}
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status):
    """Отрисовка бейджа статуса"""
    status_classes = {
        "Зарегистрирован": "status-registered",
        "В процессе": "status-progress", 
        "Ожидает": "status-waiting",
        "Критично": "status-critical"
    }
    
    class_name = status_classes.get(status, "status-progress")
    return f'<span class="status-badge {class_name}">{status}</span>'

def render_priority_badge(priority):
    """Отрисовка бейджа приоритета"""
    priority_classes = {
        "Высокий": "priority-high",
        "Средний": "priority-medium",
        "Низкий": "priority-low"
    }
    
    class_name = priority_classes.get(priority, "priority-medium")
    return f'<span class="status-badge {class_name}">{priority}</span>'

def render_dashboard():
    """Отрисовка дашборда"""
    months, reports_data, status_data, reports_df = load_sample_data()
    
    # Заголовок
    st.markdown("""
    <div class="section-header">
        <h1 class="section-title">Дашборд</h1>
        <p class="section-description">Обзор системы регистрации отчетов и управление процессами</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Табы
    tab1, tab2, tab3 = st.tabs([
        "Дашборд регистрации отчетов", 
        "Реестр отчетов", 
        "Запросы в работе"
    ])
    
    with tab1:
        # Метрики
        st.markdown("### Общая статистика")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_metric_card("Всего отчетов", "279", "+12% с прошлого месяца", True)
        
        with col2:
            render_metric_card("Зарегистрированы", "156", "56% от общего числа", True)
            
        with col3:
            render_metric_card("В процессе", "89", "32% от общего числа", True)
            
        with col4:
            render_metric_card("Ожидают", "34", "12% от общего числа", True)
        
        st.markdown("---")
        
        # Графики
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Динамика регистрации отчетов")
            st.caption("Количество зарегистрированных отчетов по месяцам")
            
            fig_bar = px.bar(
                x=months, 
                y=reports_data,
                color_discrete_sequence=["#228B22"]
            )
            fig_bar.update_layout(
                showlegend=False,
                xaxis_title="Месяц",
                yaxis_title="Количество отчетов",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#2d3748"),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            fig_bar.update_xaxis(showgrid=True, gridcolor="#e2e8f0")
            fig_bar.update_yaxis(showgrid=True, gridcolor="#e2e8f0")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("#### Распределение по статусам")
            st.caption("Текущее состояние всех отчетов")
            
            fig_pie = px.pie(
                values=status_data["Количество"],
                names=status_data["Статус"],
                color_discrete_sequence=status_data["Цвет"]
            )
            fig_pie.update_layout(
                showlegend=True,
                plot_bgcolor="white",
                paper_bgcolor="white", 
                font=dict(color="#2d3748"),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Таблица отчетов
        st.markdown("#### Последние отчеты")
        st.caption("Список недавно зарегистрированных отчетов")
        
        # Обработка данных для отображения
        display_df = reports_df.copy()
        display_df["Статус"] = display_df["Статус"].apply(render_status_badge)
        display_df["Приоритет"] = display_df["Приоритет"].apply(render_priority_badge)
        
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### Реестр отчетов")
        st.caption("Полный список всех отчетов в системе с возможностями поиска и фильтрации")
        
        # Статистика реестра
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Всего отчетов", "324")
        with col2:
            render_metric_card("Зарегистрированы", "189")
        with col3:
            render_metric_card("В процессе", "98")
        with col4:
            render_metric_card("Ожидают", "37")
        
        # Фильтры
        st.markdown("#### Фильтры и поиск")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            search_term = st.text_input("🔍 Поиск отчетов...")
        with col2:
            status_filter = st.selectbox("Статус", ["Все статусы", "Зарегистрированы", "В процессе", "Ожидают"])
        with col3:
            dept_filter = st.selectbox("Департамент", ["Все департаменты", "Финансы", "Продажи", "HR", "Маркетинг", "IT"])
        with col4:
            type_filter = st.selectbox("Тип отчета", ["Все типы", "Финансовый", "Операционный", "Аналитический"])
        with col5:
            st.button("📥 Экспорт")
        
        # Расширенная таблица
        st.markdown("#### Список отчетов")
        st.caption(f"Найдено {len(reports_df)} отчетов")
        st.dataframe(reports_df, use_container_width=True)
    
    with tab3:
        st.markdown("#### Запросы в работе")
        st.caption("Активные задачи и процессы по регистрации отчетов")
        
        # Статистика задач
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Всего задач", "23")
        with col2:
            render_metric_card("Критичные", "5")
        with col3:
            render_metric_card("В процессе", "12")
        with col4:
            render_metric_card("Ожидают", "6")
        
        # Список задач
        st.markdown("#### Активные задачи")
        
        tasks_data = {
            "ID": ["TASK-001", "TASK-002", "TASK-003"],
            "Задача": [
                "Валидация финансового отчета Q4",
                "Согласование HR отчета", 
                "Корректировка атрибутов отчета"
            ],
            "Исполнитель": ["Иванова А.П.", "Козлова Е.М.", "Морозов П.К."],
            "Статус": ["В процессе", "Ожидает", "Критично"],
            "Прогресс": ["65%", "25%", "0%"],
            "Срок": ["2024-02-20", "2024-02-25", "2024-02-21"]
        }
        
        tasks_df = pd.DataFrame(tasks_data)
        st.dataframe(tasks_df, use_container_width=True)

def main():
    """Главная функция приложения"""
    load_css()
    
    # Рендерим боковую панель и получаем выбранную страницу
    selected_page = render_sidebar()
    
    # Рендерим контент в зависимости от выбранной страницы
    if selected_page == "dashboard":
        render_dashboard()
    elif selected_page == "training":
        st.title("📚 Обучение")
        st.info("Раздел обучения находится в разработке")
    elif selected_page == "process":
        st.title("🔄 Этапы процесса")
        st.info("Раздел этапов процесса находится в разработке")
    elif selected_page == "upload":
        st.title("📤 Загрузка атрибутов")
        st.info("Раздел загрузки атрибутов находится в разработке")
    elif selected_page == "faq":
        st.title("❓ Часто задаваемые вопросы")
        st.info("Раздел FAQ находится в разработке")
    elif selected_page == "feedback":
        st.title("💬 Обратная связь")
        st.info("Раздел обратной связи находится в разработке")

if __name__ == "__main__":
    main()