from django.shortcuts import render
from .models import Card

# Library imports for well 3D-line graph function
from azure.storage.blob import ContainerClient
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

# Create your views here.

# Function for well 3D-line graph
def return_graph():

    try:
        print('...initialize Azure Connection...')

        # Create Container Client
        print('...creating container client...')
        sas_url = 'https://datavillagesa.blob.core.windows.net/volve?sv=2021-08-06&se=2023-01-24T04%3A44%3A28Z&sr=c&sp=rl&sig=X52rhtP2mhKvY4JdqWwKDpmvaVQqhrctqnoFHT%2Bpyvs%3D'
        container_client = ContainerClient.from_container_url(sas_url)
        print('Container Name: ' + container_client.container_name)
        print('...container client created...')

        # Create Blob Client
        print('...creating blob client...')
        blob_name = 'WITSML Realtime drilling data/Norway-Statoil-NO 15_$47$_9-F-15/1/trajectory/1.xml'
        blob_client = container_client.get_blob_client(blob=blob_name )
        print('...block client created...')

        # Download Blob
        print('...downloading blob...')
        blob_download = blob_client.download_blob()
        print('...blob download completed...')

        # Read Blob / WITSML File
        print('...reading blob download...')
        blob_data = blob_download.readall().decode("utf-8")
        print('...blob download read completed...')

        # Parse XML Tag
        print('...parsing xml...')
        blob_xml = BeautifulSoup(blob_data, 'xml')
        blob_tag = set(str(tag.name) for tag in blob_xml.find_all())
        print('...xml parsed...')

        # Create Panda Dataframe
        print('...creating dataframe...')
        columns = ['azi', 'md', 'tvd', 'incl']
        df = pd.DataFrame()
        for col in columns:
            df[col] = [float(x.text) for x in blob_xml.find_all(col)]
        print('...dataframe created...')
        print('...finish...')

        # Create DataFrame For Multiple Wells
        print('...creating multiple dataframe...')
        wells = ['9-F-12',
                 '9-F-14',
                 '9-F-15',
                 '9-F-11',
                 '9-F-9',
                 '9-F-7',
                 '9-F-5',
                 '9-F-4',
                 '9-F-1 C']
        columns = ['azi', 'md', 'tvd', 'incl', 'dispNs', 'dispEw']
        df_all_wells = pd.DataFrame()
        for well in wells:
            df = pd.DataFrame()
            blob_name = 'WITSML Realtime drilling data/Norway-Statoil-NO 15_$47$_' + well + '/1/trajectory/1.xml'
            blob_client = container_client.get_blob_client(blob=blob_name )
            blob_download = blob_client.download_blob()
            blob_data = blob_download.readall().decode("utf-8")
            blob_xml = BeautifulSoup(blob_data, 'xml')
            for col in columns:
                df[col] = [float(x.text) for x in blob_xml.find_all(col)]
            df['Well'] = well
            df_all_wells = pd.concat([df_all_wells, df], ignore_index=True)
        df_all_wells['neg_tvd'] = df_all_wells['tvd']*-1
        fig = px.line_3d(df_all_wells, 'dispNs', 'dispEw', 'neg_tvd', 'Well')
        print('...multiple dataframe completed...')

    except Exception as ex:
        print('Exception:')
        print(ex)

    return fig.to_html()

# Homepage
def home(request):
    # Create query object from Card class
    c = Card.objects.get(id=1)
    c.save()

    # Create context from query object
    context = {
        'name': 'Wan Ilmie ',
        'title': 'portfolio',
        'card_title': c.title,
        'card_text': c.text,
        'link_findOutMore': c.card_link(),
        'num_day': c.num_day()
    }

    return render(request, 'myapp/home.html', context)

# Volve Field Data Set Page
def volveFieldDataSet(request):

    # Create query object from Card class
    card_list = Card.objects.all()

    # Create context from query object
    context = {
        'name': 'Wan Ilmie',
        'title': 'portfolio',
        'graph': return_graph()
    }
    
    # Iterate query object and append into context
    n = len(Card.objects.all())
    for i in range(n):
        k = 'c'+str(i+1)
        context[k] = Card.objects.get(id=i+1)
    
    # Published date from most recent card
    context['num_day'] = card_list[n-1].num_day()
    print('...page load completed...')

    return render(request, 'myapp/VolveFieldDataSet.html', context)
