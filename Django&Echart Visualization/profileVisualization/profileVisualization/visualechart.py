from __future__ import unicode_literals
import math, random

from Model.linkedinModels import Skills, Profile, Education, Workingexperience

from django.shortcuts import render

from django.http import HttpResponse

from pyecharts import Line3D, Style, WordCloud, Radar, Graph

from pyecharts.constants import DEFAULT_HOST

style = Style(
    title_color="#FFF",
    title_pos="left",
    width=800,
    height=600,
    background_color='transparent',
    #color=['#87cefa', 'rgba(123,123,123,0.5)']
)

entity_name_equal={"Hong Kong University of Science and Technology":["HKUST"]}



def make_map(name = "",size=5,category='',p_id = 0):
    entity_map = {}
    entity_map["name"] = name
    entity_map["category"] = category
    entity_map["symbolSize"] = size
    entity_map["draggable"] = "False"
    entity_map["value"] = p_id
    entity_map["label"] = {"normal": {"show": "True"}}
    return entity_map

def index(request):
    if 'id' not in request.GET:
        l3d = line3d()
        ctx = {}
        script = l3d.render_embed()
        index = script.find("</script>")
        click_function = 'var theUrl = "goodbye";var xmlHttp = new XMLHttpRequest(); xmlHttp.open("GET", theUrl, true);'
        string_of_click = "myChart_"+l3d.chart_id+".on('click', function (params) {"+click_function+"console.log(params.name)});"
        string_of_click = script[:index] + string_of_click + script[index:]
        ctx['myechart'] = string_of_click
        ctx['host'] = DEFAULT_HOST
        ctx['script_list'] = l3d.get_js_dependencies()
        return render(request, "hello.html", ctx)
    elif request.GET['method']=='keyword':
        print request.GET['id']
        wordcloud = wordcloud_graph(request.GET['id'])
        ctx = {}
        script = wordcloud.render_embed()
        index = script.find("</script>")
        click_function = 'var theUrl = "goodbye";var xmlHttp = new XMLHttpRequest(); xmlHttp.open("GET", theUrl, true);'
        string_of_click = ""#"myChart_"+wordcloud.chart_id+".on('click', function (params) {"+click_function+"console.log(params.name)});"
        string_of_click = script[:index] + string_of_click + script[index:]
        ctx['myechart'] = string_of_click
        ctx['host'] = DEFAULT_HOST
        ctx['script_list'] = wordcloud.get_js_dependencies()
        ctx['hidden'] = '["keyword"]'
        return render(request, "echart_template.html", ctx)
    elif request.GET['method']=='relation':
        relation = relation_graph(request.GET['id'])
        ctx = {}
        script = relation.render_embed()
        index = script.find("</script>")
        #click_function = 'var theUrl = "/goodbye?id=5"; var xmlHttp = new XMLHttpRequest(); xmlHttp.open("GET", theUrl, true);'
        click_function = 'parent.graph(params.value,["radar","keyword"],[]);'
        string_of_click = "myChart_" + relation.chart_id + ".on('click', function (params) {" + click_function + "console.log(params.value)});"
        string_of_click = script[:index] + string_of_click + script[index:]
        ctx['myechart'] = string_of_click
        ctx['host'] = DEFAULT_HOST
        ctx['script_list'] = relation.get_js_dependencies()
        ctx['hidden'] = '["relation"]'
        return render(request, "echart_template.html", ctx)
        #return HttpResponse(string_of_click)
    elif request.GET['method']=='radar':
        radar = radar_graph(request.GET['id'])
        ctx = {}
        script = radar.render_embed()
        index = script.find("</script>")
        # click_function = 'var theUrl = "/goodbye?id=5"; var xmlHttp = new XMLHttpRequest(); xmlHttp.open("GET", theUrl, true);'
        click_function = 'parent.graph(params.value,"radar",[]);'
        string_of_click = ""#"myChart_" + radar.chart_id + ".on('click', function (params) {" + click_function + "console.log(params.value)});"
        string_of_click = script[:index] + string_of_click + script[index:]
        ctx['myechart'] = string_of_click
        ctx['host'] = DEFAULT_HOST
        ctx['script_list'] = radar.get_js_dependencies()
        ctx['hidden'] = '["radar"]'
        return render(request, "echart_template.html", ctx)

def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo", width=1200, height=600)
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d

def relation_graph(id):
    _data = {"nodes":[],"link":[],"category":[]}
    people = Profile.objects.filter(p_id=id)
    for person in people:
        _data["nodes"].append(make_map(person.name,50,person.name,id))
        _data["category"].append({"name":person.name})
        companies = Workingexperience.objects.filter(p_id=id)
        for com in companies:
            _data["nodes"].append(make_map(com.company_name,30,com.company_name,com.p_id))
            _data["category"].append({"name":com.company_name})
            _data["link"].append({"source":person.name,"target":com.company_name})
            sub_people = Profile.objects.filter(workingexperience__company_name__icontains=com.company_name).distinct()
            data_people = []
            for sub_person in sub_people:
                if sub_person not in people:
                    data_people.append((sub_person.p_id,sub_person.name))#{"name":sub_person.name,"p_id":sub_person.p_id})
            if com.company_name in entity_name_equal:
                for equal_name in entity_name_equal[com.company_name]:
                    print equal_name
                    add_people = Profile.objects.filter(workingexperience__company_name__icontains=equal_name).distinct()
                    for add_person in add_people:
                        if add_person not in people:
                            data_people.append((add_person.p_id,add_person.name))#{"name": add_person.name, "p_id": add_person.p_id})
            data_people = list(set(data_people))
            for sub_person in data_people:
                _data["nodes"].append(make_map(sub_person[1],10,com.company_name,sub_person[0]))
                    #_data["category"]
                _data["link"].append({"source":com.company_name,"target":sub_person[1]})
    graph = Graph(width=1200, height=800, background_color='transparent')
    graph.add("Person-Company", _data["nodes"], _data["link"], _data["category"],
              label_pos="right",
              graph_repulsion=50, is_legend_show=False,
              line_curve=0.2, label_text_color=None, legend_text_size='20')
    return graph

#def radar_graph(id):
#    _data = {"name":[]}

def radar_graph(p_id_):
    c_schema = []
    c_value = []
    v = []
    max = 90
    min = 0
    skill_list = []
    name = Profile.objects.filter(p_id = p_id_)[0].name
    temp = Skills.objects.filter(p_id = p_id_)
    for item in temp:
        skill_list.append((item.skill_name, item.endorsement))
    for item in skill_list:
        dic = {}
        dic['name'] = item[0]
        dic['max'] = max
        dic['min'] = min
        v.append(int(item[1]))
        c_schema.append(dic)
    c_value.append(v)
    radar = Radar(**style.init_style)
    radar.config(c_schema=c_schema, shape='polygon', radar_text_size=16, radar_text_color='white', is_area_show=True,
                 area_color="#EAEAEA", area_opacity=0.2)
    radar.add(name, c_value, item_color="#00CDCD", symbol=None, is_area_show=True, area_color="#00CDCD",
              area_opacity=0.2, legend_text_size='20', legend_text_color='white')
    return radar


def wordcloud_graph(id):
    _data = {"name":[],"value":[]}
    people = Profile.objects.filter(p_id=id)
    for person in people:
        _data["name"].append(str(person.occupation))
        _data["value"].append(random.randint(0,50))
        #_data["name"].append(str(person.location))
        #_data["value"].append(random.randint(0,50))

    people = Skills.objects.filter(p_id=id)
    for person in people:
        _data["name"].append(str(person.skill_name))
        _data["value"].append(random.randint(0,50))

    people = Education.objects.filter(p_id=id)
    for person in people:
        _data["name"].append(str(person.school_name.encode('utf-8')))
        _data["value"].append(random.randint(0, 50))
        _data["name"].append(str(person.field_study.encode('utf-8')))
        _data["value"].append(random.randint(0, 50))
        _data["name"].append(str(person.degree_name.encode('utf-8')))
        _data["value"].append(random.randint(0, 20))

    people = Workingexperience.objects.filter(p_id=id)
    for person in people:
        _data["name"].append(str(person.company_name))
        _data["value"].append(random.randint(0,50))


    print _data['name'],_data['value']

    wordcloud = WordCloud(**style.init_style)
    wordcloud.add("", _data['name'], _data['value'], word_size_range=[20, 40],shape=['diamond', 'circle', 'triangle'])#, legend_text_size='20', legend_text_color='white')#, rotate_step = 300)
    return wordcloud
