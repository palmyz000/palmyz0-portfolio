from django.shortcuts import render

# ข้อมูลจำลองสำหรับใช้งานในทุกหน้า
DATA = {
    'name': 'ชื่อ-นามสกุล ของคุณ',
    'title': 'Data Scientist / AI Engineer',
    'email': 'hello@example.com',
    'linkedin': 'linkedin.com/in/yourprofile',
    'github': 'github.com/yourusername',
    'about': 'นักวิทยาศาสตร์ข้อมูลและวิศวกรปัญญาประดิษฐ์ที่มีความหลงใหลในการใช้ข้อมูลเพื่อแก้ปัญหาทางธุรกิจและการสร้างนวัตกรรมใหม่ๆ มีประสบการณ์ในการพัฒนาโมเดล Machine Learning และนำไปใช้งานจริง',
    'experiences': [
        {
            'role': 'Senior Data Scientist',
            'company': 'Tech Solutions Co., Ltd.',
            'period': '2023 - Present',
            'description': 'ออกแบบและพัฒนา Recommendation System เพื่อเพิ่มยอดขาย 15% และสร้าง Dashboard สำหรับผู้บริหาร'
        },
        {
            'role': 'AI Engineer',
            'company': 'Startup AI',
            'period': '2020 - 2023',
            'description': 'พัฒนา Computer Vision Model สำหรับการตรวจสอบคุณภาพสินค้าในโรงงาน ลดของเสียได้ 20%'
        }
    ],
    'educations': [
        {
            'degree': 'M.S. in Data Science',
            'university': 'Top University',
            'period': '2018 - 2020'
        },
        {
            'degree': 'B.E. in Computer Engineering',
            'university': 'Tech Institute',
            'period': '2014 - 2018'
        }
    ],
    'projects': [
        {
            'title': 'Customer Churn Prediction',
            'description': 'โมเดล Machine Learning เพื่อทำนายพฤติกรรมการยกเลิกบริการของลูกค้า พร้อมให้คำแนะนำแคมเปญการตลาดที่เหมาะสม',
            'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=600',
            'tags': ['Python', 'XGBoost', 'Pandas', 'Scikit-learn']
        },
        {
            'title': 'Automated Defect Detection',
            'description': 'ระบบ AI สำหรับตรวจหาตำหนิบนชิ้นส่วนอิเล็กทรอนิกส์แบบ Real-time โดยใช้เทคนิค Deep Learning',
            'image': 'https://images.unsplash.com/photo-1620825937374-87fc7d62828e?auto=format&fit=crop&q=80&w=600',
            'tags': ['PyTorch', 'OpenCV', 'YOLO', 'Docker']
        },
        {
            'title': 'Internal Knowledge Base RAG Chatbot',
            'description': 'สร้าง Chatbot ภายในองค์กรที่สามารถดึงข้อมูลจากเอกสารนโยบายและคู่มือต่างๆ มาตอบคำถามพนักงานได้อย่างแม่นยำ',
            'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=600',
            'tags': ['LangChain', 'FastAPI', 'LLMs', 'VectorDB']
        }
    ],
    'skills': [
        {
            'category': 'Data Science & Machine Learning',
            'items': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch']
        },
        {
            'category': 'Cloud & Backend Architecture',
            'items': ['Google Cloud Platform', 'BigQuery', 'Looker', 'Cloud Run', 'FastAPI', 'AWS']
        },
        {
            'category': 'ML Engineering & Tools',
            'items': ['Docker', 'MLflow', 'Git', 'Python', 'SQL', 'PostgreSQL']
        }
    ],
    'certifications': [
        'IBM Data Science Professional Certificate',
        'DeepLearning.AI PyTorch for Deep Learning Professional Certificate'
    ],
    'awards': [
        {
            'title': 'Silver Medal',
            'event': 'Thailand New Gen Inventors Award 2025',
            'description': 'PHQ-9 Speech to text: Speech and Text Data Analysis for Depression'
        }
    ]
}

def about(request):
    return render(request, 'portfolio/about.html', DATA)

def experience(request):
    return render(request, 'portfolio/experience.html', {
        'experiences': DATA['experiences'], 
        'educations': DATA['educations'],
        'certifications': DATA['certifications'],
        'awards': DATA['awards']
    })

def projects(request):
    return render(request, 'portfolio/projects.html', {'projects': DATA['projects']})

def skills(request):
    return render(request, 'portfolio/skills.html', {'skills': DATA['skills']})

def resume(request):
    return render(request, 'portfolio/resume.html', DATA)

def tools_list(request):
    return render(request, 'portfolio/tools.html')

def interval_timer(request):
    return render(request, 'portfolio/interval_timer.html')
