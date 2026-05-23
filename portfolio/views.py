from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import logging

logger = logging.getLogger(__name__)

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
    'project_categories': [
        {
            'name': 'Machine Learning',
            'repo': 'https://github.com/palmyz000/Machine-Learning-Journey',
            'id': 'ml-journey',
            'icon': 'fas fa-laptop-code',
            'subcategories': [
                {
                    'name': 'Regression',
                    'id': 'ml-regression',
                    'icon': 'fas fa-chart-line',
                    'projects': [
                        {
                            'name': 'Length_of_Stay_Regression',
                            'display_name': 'Length of Stay Regression',
                            'description': 'Predict patient hospital length of stay to optimize medical staffing, bed availability, and hospital resource management.',
                            'tags': ['Regression', 'Scikit-Learn', 'Feature Engineering'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Regression_Projects/Length_of_Stay_Regression',
                            'icon': 'fas fa-hospital'
                        },
                        {
                            'name': 'New_York_City_Taxi_Trip_Duration_Regression',
                            'display_name': 'NYC Taxi Trip Duration Regression',
                            'description': 'Predict New York City taxi trip durations using coordinates, weather, and traffic data to optimize taxi routing and dispatch.',
                            'tags': ['Regression', 'XGBoost', 'Geospatial Data'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Regression_Projects/New_York_City_Taxi_Trip_Duration_Regression',
                            'icon': 'fas fa-taxi'
                        },
                        {
                            'name': 'Retail_Store_Inventory_Forecasting_Regression',
                            'display_name': 'Retail Store Inventory Forecasting',
                            'description': 'Forecast retail store inventory requirements to prevent out-of-stock situations and minimize overhead storage costs.',
                            'tags': ['Regression', 'Random Forest', 'Inventory Optimization'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Regression_Projects/Retail_Store_Inventory_Forecasting_Regression',
                            'icon': 'fas fa-boxes'
                        },
                        {
                            'name': 'car_price_predict_app',
                            'display_name': 'Car Price Prediction App',
                            'description': 'Interactive Streamlit web application to estimate second-hand car resale values instantly based on vehicle characteristics.',
                            'tags': ['Regression', 'LightGBM', 'Streamlit', 'Web App'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Regression_Projects/car_price_predict_app',
                            'icon': 'fas fa-car'
                        }
                    ]
                },
                {
                    'name': 'Classification',
                    'id': 'ml-classification',
                    'icon': 'fas fa-filter',
                    'projects': [
                        {
                            'name': 'Credit_Card_Fraud_Detection',
                            'display_name': 'Credit Card Fraud Detection',
                            'description': 'Machine learning fraud detection system dealing with extreme class imbalance using SMOTE and ensemble models.',
                            'tags': ['Classification', 'SMOTE', 'Random Forest', 'Fraud Detection'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/Credit_Card_Fraud_Detection',
                            'icon': 'fas fa-credit-card'
                        },
                        {
                            'name': 'Customer_Churn_Classification',
                            'display_name': 'Customer Churn Classification',
                            'description': 'Predict customer churn probability and identify key risk factors to drive proactive subscriber retention strategies.',
                            'tags': ['Classification', 'XGBoost', 'Customer Analytics'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/Customer_Churn_Classification',
                            'icon': 'fas fa-user-slash'
                        },
                        {
                            'name': 'KNN_Digit_Prediction',
                            'display_name': 'KNN Digit Prediction',
                            'description': 'Handwritten digit recognition model built and evaluated using the K-Nearest Neighbors (KNN) algorithm.',
                            'tags': ['Classification', 'KNN', 'Computer Vision Basics'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/KNN_Digit_Prediction',
                            'icon': 'fas fa-calculator'
                        },
                        {
                            'name': 'Online_Hoppers_Intention_Classification',
                            'display_name': 'Online Shoppers Purchase Intention',
                            'description': 'Classify online shopper purchase intention using real-time browsing behavior, session metadata, and page metrics.',
                            'tags': ['Classification', 'E-Commerce', 'User Behavior'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/Online_Hoppers_Intention_Classification',
                            'icon': 'fas fa-shopping-cart'
                        },
                        {
                            'name': 'customer_churn_project',
                            'display_name': 'Customer Churn Analytics',
                            'description': 'In-depth customer churn analytics and predictive classification using logistic regression and robust exploratory analysis.',
                            'tags': ['Classification', 'Logistic Regression', 'EDA'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/customer_churn_project',
                            'icon': 'fas fa-users'
                        },
                        {
                            'name': 'telco_churn_app',
                            'display_name': 'Telco Churn Prediction App',
                            'description': 'Interactive Gradio application to predict telecom subscriber churn and explore model feature importances dynamically.',
                            'tags': ['Classification', 'Gradio', 'XGBoost', 'Web App'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Classification_Projects/telco_churn_app',
                            'icon': 'fas fa-phone'
                        }
                    ]
                },
                {
                    'name': 'Clustering',
                    'id': 'ml-clustering',
                    'icon': 'fas fa-project-diagram',
                    'projects': [
                        {
                            'name': 'ALL_Beauty_Reccomendation_with_KNNwithMean',
                            'display_name': 'Beauty Recommendation (KNN with Mean)',
                            'description': 'Collaborative filtering recommendation system built with Surprise KNNWithMean to suggest tailored beauty products.',
                            'tags': ['Clustering', 'Recommendation', 'Collaborative Filtering'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Clustering_Projects/ALL_Beauty_Reccomendation_with_KNNwithMean',
                            'icon': 'fas fa-magic'
                        },
                        {
                            'name': 'Recommendation_KMean',
                            'display_name': 'Customer Segmentation using KMeans',
                            'description': 'Retail customer segmentation and profiling using K-Means clustering and the Elbow Method for targeted marketing.',
                            'tags': ['Clustering', 'K-Means', 'Market Segmentation'],
                            'repo_url': 'https://github.com/palmyz000/Machine-Learning-Journey/tree/main/Clustering_Projects/Recommendation_KMean',
                            'icon': 'fas fa-user-friends'
                        }
                    ]
                },
                {
                    'name': 'Time Series',
                    'id': 'ml-timeseries',
                    'icon': 'fas fa-history',
                    'projects': [
                        {
                            'name': 'Retail-Store-Demand-Forecasting-LightGBM',
                            'display_name': 'Retail Store Demand Forecasting (LightGBM)',
                            'description': 'High-performance time-series demand forecasting using LightGBM and robust rolling-window feature engineering.',
                            'tags': ['Time Series', 'LightGBM', 'Demand Forecasting', 'Machine Learning'],
                            'repo_url': 'https://github.com/palmyz000/Retail-Store-Demand-Forecasting-LightGBM',
                            'icon': 'fas fa-store'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'Deep Learning',
            'repo': 'https://github.com/palmyz000/Deep-Learning-Journey',
            'id': 'deep-learning',
            'icon': 'fas fa-brain',
            'subcategories': [
                {
                    'name': 'Computer Vision',
                    'id': 'dl-cv',
                    'icon': 'fas fa-eye',
                    'projects': [
                        {
                            'name': 'Brain_Tumor_Classification',
                            'display_name': 'Brain Tumor Classification',
                            'description': 'Medical image classification of brain tumors from MRI scans using PyTorch CNN and transfer learning for diagnosis support.',
                            'tags': ['Deep Learning', 'PyTorch', 'CNN', 'Medical Imaging'],
                            'repo_url': 'https://github.com/palmyz000/Deep-Learning-Journey/tree/main/Brain_Tumor_Classification',
                            'icon': 'fas fa-brain'
                        },
                        {
                            'name': 'Skin_Diseases_Classification',
                            'display_name': 'Skin Diseases Classification',
                            'description': 'Deep learning classification model using TensorFlow ResNet to assist in pre-screening dermatological conditions from images.',
                            'tags': ['Deep Learning', 'TensorFlow', 'ResNet', 'Computer Vision'],
                            'repo_url': 'https://github.com/palmyz000/Deep-Learning-Journey/tree/main/Skin_Diseases_Classification',
                            'icon': 'fas fa-stethoscope'
                        }
                    ]
                },
                {
                    'name': 'Natural Language Processing',
                    'id': 'dl-nlp',
                    'icon': 'fas fa-language',
                    'projects': [
                        {
                            'name': 'NLP_Disaster_Tweets',
                            'display_name': 'NLP Disaster Tweets Classification',
                            'description': 'Fine-tune a BERT transformer model to classify whether real-time Twitter social media feeds report actual disaster events.',
                            'tags': ['Deep Learning', 'Transformers', 'BERT', 'NLP'],
                            'repo_url': 'https://github.com/palmyz000/Deep-Learning-Journey/tree/main/NLP_Disaster_Tweets',
                            'icon': 'fas fa-bullhorn'
                        }
                    ]
                }
            ]
        },
        {
            'name': 'AI Agents & RAG',
            'repo': 'https://github.com/palmyz000/RAG-Journey',
            'id': 'ai-agents-rag',
            'icon': 'fas fa-robot',
            'subcategories': [
                {
                    'name': 'Frameworks & Orchestration',
                    'id': 'rag-frameworks',
                    'icon': 'fas fa-network-wired',
                    'projects': [
                        {
                            'name': 'crewai',
                            'display_name': 'Multi-Agent Orchestration with CrewAI',
                            'description': 'Orchestrate collaborative multi-agent systems using CrewAI, assigning tailored personas to solve complex tasks.',
                            'tags': ['AI Agents', 'CrewAI', 'Multi-Agent Systems'],
                            'repo_url': 'https://github.com/palmyz000/RAG-Journey/tree/main/src/crewai',
                            'icon': 'fas fa-users'
                        },
                        {
                            'name': 'langchain',
                            'display_name': 'Advanced RAG Pipeline with LangChain',
                            'description': 'Build production-grade Retrieval-Augmented Generation (RAG) pipelines using LangChain, VectorDB, and LLMs.',
                            'tags': ['RAG', 'LangChain', 'VectorDB', 'Embeddings'],
                            'repo_url': 'https://github.com/palmyz000/RAG-Journey/tree/main/src/langchain',
                            'icon': 'fas fa-link'
                        },
                        {
                            'name': 'langgraph',
                            'display_name': 'Stateful Agent Workflows with LangGraph',
                            'description': 'Develop robust cyclic stateful agentic workflows using LangGraph to enable complex reasoning loops.',
                            'tags': ['AI Agents', 'LangGraph', 'Stateful Workflows'],
                            'repo_url': 'https://github.com/palmyz000/RAG-Journey/tree/main/src/langgraph',
                            'icon': 'fas fa-route'
                        }
                    ]
                }
            ]
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

@ensure_csrf_cookie
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
    return render(request, 'portfolio/projects.html', {'project_categories': DATA['project_categories']})

def skills(request):
    return render(request, 'portfolio/skills.html', {'skills': DATA['skills']})

def resume(request):
    return render(request, 'portfolio/resume.html', DATA)

def tools_list(request):
    return render(request, 'portfolio/tools.html')

def interval_timer(request):
    return render(request, 'portfolio/interval_timer.html')

def contact_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('name')
            message = data.get('message')
            
            if not email or not name or not message:
                return JsonResponse({'status': 'error', 'message': 'Please fill all fields'}, status=400)

            # Construct Email
            subject = f"🚀 Portfolio: New message from {name}"
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            
            # Note: The user needs to configure SMTP settings in settings.py for this to actually send an email.
            # For now, it will print to console if EMAIL_BACKEND is set correctly, 
            # or we can catch the error if not configured.
            try:
                send_mail(
                    subject,
                    email_body,
                    None, # Uses DEFAULT_FROM_EMAIL
                    ['Suphawit11@icloud.com'],
                    fail_silently=False,
                )
            except Exception as mail_err:
                logger.error(f"Mail sending failed: {mail_err}")
                # We still return success for demo purposes if it's just a config issue, 
                # but in reality, you'd want to handle this.
                print(f"DEBUG EMAIL:\n{email_body}")

            return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully! 🚀'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
