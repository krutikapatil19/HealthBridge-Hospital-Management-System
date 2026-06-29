from django.core.management.base import BaseCommand
from core.models import Hospital, Department, Doctor


PUNE_HOSPITALS = [
    {
        'name': 'Ruby Hall Clinic',
        'area': 'Shivajinagar',
        'address': '40, Sassoon Road, Shivajinagar, Pune - 411001',
        'phone': '020-26163391',
        'email': 'info@rubyhall.com',
        'description': "One of Pune's premier multi-specialty hospitals with over 400 beds. Known for cardiac, neurology and oncology care.",
        'total_beds': 420, 'available_beds': 87, 'icu_beds': 60, 'available_icu_beds': 12,
        'rating': 4.5, 'established_year': 1959, 'emergency': True,
        'latitude': 18.5285, 'longitude': 73.8742,
        'image_url': 'https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80',
        'departments': ['Cardiology','Neurology','Orthopedics','Oncology','General Medicine','Emergency','Gynecology','Pediatrics','Dermatology','Urology'],
        'doctors': [
            {'name':'Rajiv Sharma',    'dept':'Cardiology',      'qual':'MD, DM Cardiology',          'exp':22,'fee':800},
            {'name':'Meera Joshi',     'dept':'Neurology',       'qual':'MD, DM Neurology',           'exp':18,'fee':750},
            {'name':'Sanjay Kulkarni', 'dept':'Orthopedics',     'qual':'MS Ortho, Joint Replacement','exp':15,'fee':600},
            {'name':'Priya Deshmukh',  'dept':'Oncology',        'qual':'MD, DM Oncology',            'exp':20,'fee':950},
            {'name':'Anil Bhatt',      'dept':'General Medicine','qual':'MD General Medicine',        'exp':17,'fee':500},
            {'name':'Kavita Nair',     'dept':'Emergency',       'qual':'MD Emergency Medicine',      'exp':12,'fee':400},
            {'name':'Sunita Patil',    'dept':'Gynecology',      'qual':'MS Gynecology, DGO',         'exp':19,'fee':700},
            {'name':'Rohit Mehta',     'dept':'Pediatrics',      'qual':'MD Pediatrics, DCH',         'exp':14,'fee':600},
            {'name':'Sneha Wagh',      'dept':'Dermatology',     'qual':'MD Dermatology',             'exp':11,'fee':550},
            {'name':'Deepak Joshi',    'dept':'Urology',         'qual':'MS Urology, MCh',            'exp':16,'fee':800},
        ]
    },
    {
        'name': 'Jehangir Hospital',
        'area': 'Shivajinagar',
        'address': '32, Sassoon Road, Shivajinagar, Pune - 411001',
        'phone': '020-66819999',
        'email': 'info@jehangirhospital.com',
        'description': 'A 300-bed multispeciality hospital offering comprehensive healthcare services with cutting-edge technology.',
        'total_beds': 300, 'available_beds': 54, 'icu_beds': 40, 'available_icu_beds': 8,
        'rating': 4.4, 'established_year': 1946, 'emergency': True,
        'latitude': 18.5278, 'longitude': 73.8729,
        'image_url': 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80',
        'departments': ['Cardiology','Gynecology','Pediatrics','General Medicine','Dermatology','ENT','Orthopedics','Neurology','Ophthalmology','Psychiatry'],
        'doctors': [
            {'name':'Anita Desai',    'dept':'Gynecology',      'qual':'MD Obstetrics & Gynecology','exp':20,'fee':700},
            {'name':'Prakash Mehta',  'dept':'Pediatrics',      'qual':'MD Pediatrics',             'exp':16,'fee':600},
            {'name':'Kavita Patil',   'dept':'Dermatology',     'qual':'MD Dermatology',            'exp':12,'fee':550},
            {'name':'Vivek Kulkarni', 'dept':'Cardiology',      'qual':'DM Cardiology',             'exp':21,'fee':850},
            {'name':'Rashmi Iyer',    'dept':'General Medicine','qual':'MD General Medicine',       'exp':14,'fee':450},
            {'name':'Suhas Deshpande','dept':'ENT',             'qual':'MS ENT',                    'exp':13,'fee':500},
            {'name':'Nitin Joshi',    'dept':'Orthopedics',     'qual':'MS Orthopedics',            'exp':18,'fee':650},
            {'name':'Pooja Shah',     'dept':'Neurology',       'qual':'DM Neurology',              'exp':15,'fee':750},
            {'name':'Arun More',      'dept':'Ophthalmology',   'qual':'MS Ophthalmology',          'exp':11,'fee':500},
            {'name':'Shruti Gokhale', 'dept':'Psychiatry',      'qual':'MD Psychiatry',             'exp':10,'fee':600},
        ]
    },
    {
        'name': 'KEM Hospital',
        'area': 'Deccan',
        'address': 'Rasta Peth, Pune - 411011',
        'phone': '020-26128000',
        'email': 'kemhospital@pune.gov.in',
        'description': 'Sassoon General Hospital (KEM) is a government hospital providing affordable healthcare to all citizens of Pune.',
        'total_beds': 1200, 'available_beds': 210, 'icu_beds': 100, 'available_icu_beds': 22,
        'rating': 4.0, 'established_year': 1867, 'emergency': True,
        'latitude': 18.5167, 'longitude': 73.8569,
        'image_url': 'https://images.unsplash.com/photo-1580281657702-257584239a55?w=800&q=80',
        'departments': ['General Medicine','Emergency','Pediatrics','Gynecology','Orthopedics','Psychiatry','Dermatology','ENT','Ophthalmology','Neurology'],
        'doctors': [
            {'name':'Suresh Gaikwad', 'dept':'General Medicine','qual':'MD General Medicine',  'exp':25,'fee':200},
            {'name':'Priya Wagh',     'dept':'Gynecology',      'qual':'MS Gynecology',        'exp':18,'fee':200},
            {'name':'Amol Jadhav',    'dept':'Pediatrics',      'qual':'MD Pediatrics',        'exp':15,'fee':150},
            {'name':'Seema Kale',     'dept':'Psychiatry',      'qual':'MD Psychiatry',        'exp':12,'fee':200},
            {'name':'Vilas Bhosale',  'dept':'Orthopedics',     'qual':'MS Orthopedics',       'exp':20,'fee':200},
            {'name':'Rekha Nair',     'dept':'Emergency',       'qual':'MD Emergency Medicine','exp':10,'fee':100},
            {'name':'Yogesh Pawar',   'dept':'Dermatology',     'qual':'MD Dermatology',       'exp':14,'fee':150},
            {'name':'Lata Shinde',    'dept':'ENT',             'qual':'MS ENT',               'exp':16,'fee':150},
            {'name':'Vinayak More',   'dept':'Ophthalmology',   'qual':'MS Ophthalmology',     'exp':13,'fee':150},
            {'name':'Mangesh Dhole',  'dept':'Neurology',       'qual':'DM Neurology',         'exp':17,'fee':200},
        ]
    },
    {
        'name': 'Deenanath Mangeshkar Hospital',
        'area': 'Erandwane',
        'address': '28 & 29, Erandwane, Near Mhatre Bridge, Pune - 411004',
        'phone': '020-49150200',
        'email': 'info@deenanathmangeshhospital.org',
        'description': 'A super-specialty hospital known for liver transplants, cardiac surgery and robotic surgery. 600+ beds.',
        'total_beds': 620, 'available_beds': 95, 'icu_beds': 80, 'available_icu_beds': 14,
        'rating': 4.6, 'established_year': 1958, 'emergency': True,
        'latitude': 18.5103, 'longitude': 73.8376,
        'image_url': 'https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80',
        'departments': ['Cardiology','Gastroenterology','Urology','Neurology','Oncology','Orthopedics','Gynecology','Pediatrics','Nephrology','Pulmonology'],
        'doctors': [
            {'name':'Abhijit Deshpande','dept':'Gastroenterology','qual':'DM Gastroenterology',       'exp':24,'fee':900},
            {'name':'Neha Gokhale',    'dept':'Cardiology',      'qual':'DM Cardiology',              'exp':19,'fee':850},
            {'name':'Rahul Bhosale',   'dept':'Urology',         'qual':'MS Urology, MCh',            'exp':17,'fee':800},
            {'name':'Asmita Joshi',    'dept':'Neurology',       'qual':'DM Neurology',               'exp':22,'fee':900},
            {'name':'Pramod Kulkarni', 'dept':'Oncology',        'qual':'MD, DM Oncology',            'exp':20,'fee':1000},
            {'name':'Sangeeta Rao',    'dept':'Orthopedics',     'qual':'MS Orthopedics',             'exp':15,'fee':700},
            {'name':'Meghna Patil',    'dept':'Gynecology',      'qual':'MS Gynecology, FRM',         'exp':18,'fee':800},
            {'name':'Tejas Shah',      'dept':'Pediatrics',      'qual':'MD Pediatrics, Neonatology', 'exp':14,'fee':700},
            {'name':'Varsha Desai',    'dept':'Nephrology',      'qual':'DM Nephrology',              'exp':16,'fee':850},
            {'name':'Kiran Mehta',     'dept':'Pulmonology',     'qual':'DM Pulmonology',             'exp':13,'fee':750},
        ]
    },
    {
        'name': 'Poona Hospital and Research Centre',
        'area': 'Sadashiv Peth',
        'address': '27, Sadashiv Peth, Tilak Road, Pune - 411030',
        'phone': '020-24331099',
        'email': 'info@poonahospital.org',
        'description': 'A 300-bed charitable hospital providing quality healthcare at affordable rates since 1984.',
        'total_beds': 300, 'available_beds': 62, 'icu_beds': 35, 'available_icu_beds': 9,
        'rating': 4.2, 'established_year': 1984, 'emergency': True,
        'latitude': 18.5121, 'longitude': 73.8584,
        'image_url': 'https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&q=80',
        'departments': ['General Medicine','Orthopedics','Gynecology','Pediatrics','ENT','Cardiology','Dermatology','Ophthalmology','Psychiatry','Neurology'],
        'doctors': [
            {'name':'Vinod Joshi',    'dept':'Orthopedics',     'qual':'MS Orthopedics',      'exp':21,'fee':500},
            {'name':'Smita Naik',     'dept':'Pediatrics',      'qual':'MD Pediatrics',       'exp':14,'fee':450},
            {'name':'Ramesh Kulkarni','dept':'General Medicine','qual':'MD General Medicine', 'exp':19,'fee':400},
            {'name':'Alka Deshpande', 'dept':'Gynecology',      'qual':'MS Gynecology',       'exp':16,'fee':500},
            {'name':'Hemant Pawar',   'dept':'ENT',             'qual':'MS ENT',              'exp':12,'fee':450},
            {'name':'Nilima Bhatt',   'dept':'Cardiology',      'qual':'DM Cardiology',       'exp':18,'fee':700},
            {'name':'Sachin More',    'dept':'Dermatology',     'qual':'MD Dermatology',      'exp':10,'fee':400},
            {'name':'Usha Rao',       'dept':'Ophthalmology',   'qual':'MS Ophthalmology',    'exp':13,'fee':450},
            {'name':'Ganesh Shinde',  'dept':'Psychiatry',      'qual':'MD Psychiatry',       'exp':11,'fee':500},
            {'name':'Madhuri Wagh',   'dept':'Neurology',       'qual':'DM Neurology',        'exp':15,'fee':600},
        ]
    },
    {
        'name': 'Lokmanya Hospital',
        'area': 'Nigdi',
        'address': 'Survey No. 103/1, Mumbai-Pune Road, Chinchwad, Pune - 411033',
        'phone': '020-27655900',
        'email': 'info@lokmanyahospital.com',
        'description': 'Multi-specialty hospital serving Pimpri-Chinchwad region with 200+ beds and 24/7 emergency services.',
        'total_beds': 220, 'available_beds': 48, 'icu_beds': 30, 'available_icu_beds': 6,
        'rating': 4.3, 'established_year': 2003, 'emergency': True,
        'latitude': 18.6489, 'longitude': 73.8002,
        'image_url': 'https://images.unsplash.com/photo-1504813184591-01572f98c85f?w=800&q=80',
        'departments': ['General Medicine','Cardiology','Orthopedics','Gynecology','Neurology','Pediatrics','Dermatology','ENT','Urology','Emergency'],
        'doctors': [
            {'name':'Amar Pawar',     'dept':'Cardiology',      'qual':'DM Cardiology',        'exp':16,'fee':700},
            {'name':'Sunita More',    'dept':'General Medicine','qual':'MD Medicine',           'exp':13,'fee':400},
            {'name':'Rajan Desai',    'dept':'Orthopedics',     'qual':'MS Orthopedics',       'exp':17,'fee':600},
            {'name':'Pallavi Joshi',  'dept':'Gynecology',      'qual':'MS Gynecology',        'exp':14,'fee':550},
            {'name':'Nikhil Kulkarni','dept':'Neurology',       'qual':'DM Neurology',         'exp':12,'fee':650},
            {'name':'Swati Bhosale',  'dept':'Pediatrics',      'qual':'MD Pediatrics',        'exp':11,'fee':500},
            {'name':'Ajay Nair',      'dept':'Dermatology',     'qual':'MD Dermatology',       'exp':9, 'fee':450},
            {'name':'Priti Mehta',    'dept':'ENT',             'qual':'MS ENT',               'exp':13,'fee':500},
            {'name':'Sandip Rao',     'dept':'Urology',         'qual':'MS Urology',           'exp':15,'fee':650},
            {'name':'Kalpana Shinde', 'dept':'Emergency',       'qual':'MD Emergency Medicine','exp':10,'fee':350},
        ]
    },
    {
        'name': 'Inamdar Multispecialty Hospital',
        'area': 'Fatima Nagar',
        'address': 'Sr. No. 15, Fatima Nagar, Wanowrie, Pune - 411040',
        'phone': '020-67455000',
        'email': 'info@inamdarshospital.org',
        'description': 'NABH accredited 300-bed hospital near Hadapsar, known for cardiac and neuro excellence.',
        'total_beds': 300, 'available_beds': 71, 'icu_beds': 45, 'available_icu_beds': 11,
        'rating': 4.4, 'established_year': 2009, 'emergency': True,
        'latitude': 18.4876, 'longitude': 73.8934,
        'image_url': 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=800&q=80',
        'departments': ['Cardiology','Neurology','Orthopedics','Pediatrics','General Medicine','Dermatology','Gynecology','Urology','ENT','Ophthalmology'],
        'doctors': [
            {'name':'Kiran Talekar',    'dept':'Neurology',       'qual':'DM Neurology',        'exp':18,'fee':750},
            {'name':'Deepa Bhave',      'dept':'Pediatrics',      'qual':'MD Pediatrics, DCH',  'exp':15,'fee':600},
            {'name':'Santosh Patil',    'dept':'Cardiology',      'qual':'DM Cardiology',       'exp':20,'fee':800},
            {'name':'Archana Gaikwad',  'dept':'Orthopedics',     'qual':'MS Orthopedics',      'exp':14,'fee':650},
            {'name':'Rajesh Deshpande', 'dept':'General Medicine','qual':'MD General Medicine', 'exp':12,'fee':450},
            {'name':'Preeti Kulkarni',  'dept':'Dermatology',     'qual':'MD Dermatology',      'exp':10,'fee':500},
            {'name':'Harish Mehta',     'dept':'Gynecology',      'qual':'MS Gynecology',       'exp':17,'fee':700},
            {'name':'Shweta Rao',       'dept':'Urology',         'qual':'MS Urology',          'exp':13,'fee':700},
            {'name':'Nitin Pawar',      'dept':'ENT',             'qual':'MS ENT',              'exp':11,'fee':480},
            {'name':'Leena Joshi',      'dept':'Ophthalmology',   'qual':'MS Ophthalmology',    'exp':12,'fee':500},
        ]
    },
    {
        'name': 'Aditya Birla Memorial Hospital',
        'area': 'Wakad',
        'address': 'Thergaon, Chinchwad, Pune - 411033',
        'phone': '020-30717171',
        'email': 'info@adityabirlahospital.com',
        'description': 'A 650-bed NABH accredited hospital with state-of-the-art infrastructure and world class services.',
        'total_beds': 650, 'available_beds': 130, 'icu_beds': 90, 'available_icu_beds': 20,
        'rating': 4.5, 'established_year': 2008, 'emergency': True,
        'latitude': 18.6002, 'longitude': 73.7614,
        'image_url': 'https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80',
        'departments': ['Cardiology','Oncology','Neurology','Orthopedics','Gastroenterology','Urology','Gynecology','Pediatrics','Nephrology','Pulmonology'],
        'doctors': [
            {'name':'Siddharth Rao',    'dept':'Oncology',         'qual':'MD, DM Oncology',            'exp':22,'fee':1000},
            {'name':'Priyanka Shah',    'dept':'Gynecology',       'qual':'MS Gynecology',              'exp':17,'fee':750},
            {'name':'Narendra Kulkarni','dept':'Gastroenterology', 'qual':'DM Gastro',                  'exp':20,'fee':900},
            {'name':'Vikram Desai',     'dept':'Cardiology',       'qual':'DM Cardiology, FACC',        'exp':25,'fee':1100},
            {'name':'Ananya Bhatt',     'dept':'Neurology',        'qual':'DM Neurology',               'exp':18,'fee':900},
            {'name':'Sunil More',       'dept':'Orthopedics',      'qual':'MS Ortho, Joint Replacement','exp':21,'fee':800},
            {'name':'Kaveri Joshi',     'dept':'Urology',          'qual':'MCh Urology',                'exp':16,'fee':850},
            {'name':'Ishaan Patil',     'dept':'Pediatrics',       'qual':'MD Pediatrics, FRCPCH',      'exp':14,'fee':750},
            {'name':'Divya Nair',       'dept':'Nephrology',       'qual':'DM Nephrology',              'exp':15,'fee':900},
            {'name':'Shantanu Rane',    'dept':'Pulmonology',      'qual':'DM Pulmonology',             'exp':13,'fee':800},
        ]
    },
    {
        'name': 'Surya Mother & Child Superspeciality Hospital',
        'area': 'Baner',
        'address': 'Survey No. 95-2, Baner Road, Baner, Pune - 411045',
        'phone': '020-67229999',
        'email': 'info@suryahospital.com',
        'description': 'Specialized in mother and child healthcare including NICU, fertility treatment, and pediatric surgery.',
        'total_beds': 150, 'available_beds': 38, 'icu_beds': 20, 'available_icu_beds': 5,
        'rating': 4.7, 'established_year': 2012, 'emergency': True,
        'latitude': 18.5596, 'longitude': 73.7893,
        'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80',
        'departments': ['Gynecology','Pediatrics','General Medicine','Neonatology','Fertility','Dermatology','Psychiatry','Ophthalmology','ENT','Nutrition'],
        'doctors': [
            {'name':'Rohini Kale',     'dept':'Gynecology',     'qual':'MS OBG, Fetal Medicine',     'exp':20,'fee':1000},
            {'name':'Mahesh Bhatt',    'dept':'Pediatrics',     'qual':'MD Pediatrics, Neonatology', 'exp':18,'fee':800},
            {'name':'Varsha Patil',    'dept':'Neonatology',    'qual':'MD Neonatology',             'exp':15,'fee':850},
            {'name':'Snehal Rao',      'dept':'Fertility',      'qual':'MS OBG, IVF Specialist',     'exp':17,'fee':1200},
            {'name':'Anupama Joshi',   'dept':'General Medicine','qual':'MD General Medicine',       'exp':12,'fee':500},
            {'name':'Trupti Deshpande','dept':'Dermatology',    'qual':'MD Dermatology',             'exp':11,'fee':600},
            {'name':'Smruti Kulkarni', 'dept':'Psychiatry',     'qual':'MD Psychiatry',              'exp':13,'fee':700},
            {'name':'Sheela Mehta',    'dept':'Ophthalmology',  'qual':'MS Ophthalmology',           'exp':14,'fee':600},
            {'name':'Vinita Gaikwad',  'dept':'ENT',            'qual':'MS ENT',                     'exp':10,'fee':550},
            {'name':'Archana Shinde',  'dept':'Nutrition',      'qual':'MSc Nutrition, RD',          'exp':9, 'fee':400},
        ]
    },
    {
        'name': 'Noble Hospital',
        'area': 'Hadapsar',
        'address': '153, Magarpatta City Road, Hadapsar, Pune - 411013',
        'phone': '020-67116711',
        'email': 'info@noblehospital.org',
        'description': 'A 250-bed multi-specialty hospital serving Magarpatta and Hadapsar with round-the-clock emergency care.',
        'total_beds': 250, 'available_beds': 55, 'icu_beds': 32, 'available_icu_beds': 7,
        'rating': 4.3, 'established_year': 2006, 'emergency': True,
        'latitude': 18.4943, 'longitude': 73.9295,
        'image_url': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&q=80',
        'departments': ['General Medicine','Orthopedics','Cardiology','Dermatology','ENT','Ophthalmology','Gynecology','Pediatrics','Neurology','Emergency'],
        'doctors': [
            {'name':'Ganesh Patil',   'dept':'Orthopedics',     'qual':'MS Ortho, Joint Replacement','exp':19,'fee':650},
            {'name':'Archana Mane',   'dept':'Dermatology',     'qual':'MD Skin & VD',               'exp':12,'fee':500},
            {'name':'Abhay Kulkarni', 'dept':'Cardiology',      'qual':'DM Cardiology',              'exp':17,'fee':750},
            {'name':'Swapnil Joshi',  'dept':'General Medicine','qual':'MD General Medicine',        'exp':14,'fee':450},
            {'name':'Namrata Desai',  'dept':'ENT',             'qual':'MS ENT',                     'exp':11,'fee':480},
            {'name':'Prajakta More',  'dept':'Ophthalmology',   'qual':'MS Ophthalmology',           'exp':13,'fee':500},
            {'name':'Supriya Shah',   'dept':'Gynecology',      'qual':'MS Gynecology',              'exp':16,'fee':650},
            {'name':'Omkar Rao',      'dept':'Pediatrics',      'qual':'MD Pediatrics',              'exp':12,'fee':550},
            {'name':'Harshali Bhatt', 'dept':'Neurology',       'qual':'DM Neurology',               'exp':15,'fee':700},
            {'name':'Ajit Gaikwad',   'dept':'Emergency',       'qual':'MD Emergency Medicine',      'exp':10,'fee':350},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed Pune hospitals — 10 departments & 10 doctors each, with map coordinates and images'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help='Delete all hospitals before re-seeding')

    def handle(self, *args, **kwargs):
        if kwargs.get('reset'):
            Hospital.objects.all().delete()
            self.stdout.write(self.style.WARNING('All hospitals deleted. Re-seeding...\n'))

        self.stdout.write('Seeding Pune hospitals...\n')
        created_count = 0

        for data in PUNE_HOSPITALS:
            hospital, created = Hospital.objects.get_or_create(
                name=data['name'],
                defaults={
                    'area':               data['area'],
                    'address':            data['address'],
                    'phone':              data['phone'],
                    'email':              data['email'],
                    'description':        data['description'],
                    'total_beds':         data['total_beds'],
                    'available_beds':     data['available_beds'],
                    'icu_beds':           data['icu_beds'],
                    'available_icu_beds': data['available_icu_beds'],
                    'rating':             data['rating'],
                    'established_year':   data['established_year'],
                    'emergency':          data['emergency'],
                    'latitude':           data.get('latitude'),
                    'longitude':          data.get('longitude'),
                    'image_url':          data.get('image_url', ''),
                }
            )

            if created:
                created_count += 1
                dept_map = {}
                for dept_name in data['departments']:
                    dept = Department.objects.create(hospital=hospital, name=dept_name)
                    dept_map[dept_name] = dept

                doc_count = 0
                for doc in data.get('doctors', []):
                    dept_obj = dept_map.get(doc['dept'])
                    if dept_obj:
                        Doctor.objects.create(
                            hospital=hospital,
                            department=dept_obj,
                            name=doc['name'],
                            qualification=doc['qual'],
                            experience_years=doc['exp'],
                            consultation_fee=doc['fee'],
                        )
                        doc_count += 1

                self.stdout.write(
                    f"  + Created : {hospital.name} "
                    f"({len(data['departments'])} depts, {doc_count} doctors)"
                )
            else:
                # update image_url if missing
                if not hospital.image_url and data.get('image_url'):
                    hospital.image_url = data['image_url']
                    hospital.save(update_fields=['image_url'])
                self.stdout.write(f"  - Exists  : {hospital.name}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} hospital(s) created.'
        ))
        if created_count == 0:
            self.stdout.write(self.style.WARNING(
                'All already exist. Use --reset to re-seed.'
            ))
