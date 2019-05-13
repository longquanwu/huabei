# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, request
from huabei import HuaBei

hb = HuaBei()

app = Flask(__name__)

@app.route('/love', methods=['GET', 'POST'])
def love():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>小小 情人节快乐~</title>
<meta charset="utf-8">
</head>
<body>
<p style="text-align: center;">
<canvas id="c" height="500" width="500"></canvas>
<script>
	var b = document.body;
	var c = document.getElementsByTagName('canvas')[0];
	var a = c.getContext('2d');
	document.body.clientWidth; 
</script> 
<script>
// start of submission //
with(m=Math)C=cos,S=sin,P=pow,R=random;c.width=c.height=f=500;h=-250;function p(a,b,c){if(c>60)return[S(a*7)*(13+5/(.2+P(b*4,4)))-S(b)*50,b*f+50,625+C(a*7)*(13+5/(.2+P(b*4,4)))+b*400,a*1-b/2,a];A=a*2-1;B=b*2-1;if(A*A+B*B<1){if(c>37){n=(j=c&1)?6:4;o=.5/(a+.01)+C(b*125)*3-a*300;w=b*h;return[o*C(n)+w*S(n)+j*610-390,o*S(n)-w*C(n)+550-j*350,1180+C(B+A)*99-j*300,.4-a*.1+P(1-B*B,-h*6)*.15-a*b*.4+C(a+b)/5+P(C((o*(a+1)+(B>0?w:-w))/25),30)*.1*(1-B*B),o/1e3+.7-o*w*3e-6]}if(c>32){c=c*1.16-.15;o=a*45-20;w=b*b*h;z=o*S(c)+w*C(c)+620;return[o*C(c)-w*S(c),28+C(B*.5)*99-b*b*b*60-z/2-h,z,(b*b*.3+P((1-(A*A)),7)*.15+.3)*b,b*.7]}o=A*(2-b)*(80-c*2);w=99-C(A)*120-C(b)*(-h-c*4.9)+C(P(1-b,7))*50+c*2;z=o*S(c)+w*C(c)+700;return[o*C(c)-w*S(c),B*99-C(P(b, 7))*50-c/3-z/1.35+450,z,(1-b/1.2)*.9+a*.1, P((1-b),20)/4+.05]}}setInterval('for(i=0;i<1e4;i++)if(s=p(R(),R(),i%46/.74)){z=s[2];x=~~(s[0]*f/z-h);y=~~(s[1]*f/z-h);if(!m[q=y*f+x]|m[q]>z)m[q]=z,a.fillStyle="rgb("+~(s[3]*h)+","+~(s[4]*h)+","+~(s[3]*s[3]*-80)+")",a.fillRect(x,y,1,1)}',0)
// end of submission //
</script><br>
</body>
</html>
    '''


@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page')
    page = 1 if (page is None or int(page) < 1) else int(page)

    data = hb.get_snow_pack_list(page)
    template = ''
    i = 0
    for item in data['list']:
        template += "<div style='width=\"100%%\"' onclick=\"location='/snowPack/dayList?uuid=%s'\"><p><span>%s</span><span style='float=\"right\"'>%s</span></p><img src='%s' width='100%%' float='%s'></div><br>" % (item['uuid'], item['name'] + '(%s张)' %item['photos_count'], item['update_time'], item['cover'], 'left' if i % 2 == 0 else 'right')
        i = i + 1

    #上一页 下一页
    if page > 1:
        template = "<div style='text-align:center; color: blue' onclick=\"location='?page=%d'\">上一页</div>" %(page - 1) + template
    if data['has_next_page']:
        template = template + "<div style='text-align:center; color: green' onclick=\"location='?page=%d'\">下一页</div>" %(page + 1)

    return template

@app.route('/snowPack/dayList', methods=['GET'])
def snow_pack_day_list():
    uuid = request.args.get('uuid')
    page = request.args.get('page')
    page = 1 if (page is None or int(page) < 1) else int(page)
    data = hb.get_snow_pack_day_list(uuid, page)
    template = '<head><title>%s</title></head>' %data['title']
    i = 0
    for item in data['list']:
        template += "<div style='width=\"100%%\"' onclick=\"location='/snowPack/day/chooseTime?uuid=%s&date=%s'\"><h4>%s (%s张)</h4><img src='%s' width='100%%'></div><br>" % (uuid, item['date'], item['date'], item['count'], item['cover'])
        i = i + 1

    # 上一页 下一页
    if page > 1:
        template = "<h2 style='text-align:center; color: blue' onclick=\"location='/snowPack/dayList?uuid=%s&page=%s'\">上一页</h2>" % (uuid, page - 1) + template
    if data['has_next_page']:
        template = template + "<h2 style='text-align:center; color: green' onclick=\"location='/snowPack/dayList?uuid=%s&page=%s'\">下一页</h2>" % (uuid, page + 1)

    return template

@app.route('/snowPack/day/chooseTime', methods=['GET'])
def snow_pack_day_time_list():
    uuid = request.args.get('uuid')
    date = request.args.get('date')
    template = '<head><title>%s</title></head>' % '选择时间段'

    for key in hb.time_type:
        template += "<div style='text-align:center; font-size: 36px; padding: 20px; margin:20px; color: green; background-color: silver;' onclick=\"location='/snowPack/day/photos?uuid=%s&date=%s&apn=%s'\">%s</div>" %(uuid, date, key, hb.time_type[key])

    return template

@app.route('/snowPack/day/photos', methods=['GET'])
def photos_by_day():
    uuid = request.args.get('uuid')
    date = request.args.get('date')
    apn = request.args.get('apn')
    page = request.args.get('page')
    if page is None:
        page = 1
    page = 1 if int(page) < 1 else int(page)
    data = hb.get_snow_pack_photo_walls_by_day(uuid, date, apn, page)
    template = '<head><title>%s</title></head>' % '照片列表'
    i = 0
    for item in data['list']:
        if i % 2 == 0:
            template += "<div style='height=334px;'>"
        template += "<span style=\"width:48%%; %s\" onclick=\"location='%s'\"><img src='%s'></span>" % ('' if i % 2 == 0 else 'float:right;', item['src'], item['cover'])
        i = i + 1
        if i % 2 == 0:
            template += '</div>'

    # 上一页 下一页
    if page > 1:
        template = "<h2 style='text-align:center; color: blue' onclick=\"location='/snowPack/day/photos?uuid=%s&date=%s&apn=%s&page=%s'\">上一页</h2>" % (uuid, date, apn, page - 1) + template
    if data['has_next_page']:
        template = template + "<h2 style='text-align:center; color: green' onclick=\"location='/snowPack/day/photos?uuid=%s&date=%s&apn=%s&page=%s'\">下一页</h2>" % (uuid, date, apn, page + 1)

    return template

@app.route('/snowPack/recommend', methods=['GET'])
def snow_pack_recommend():
    uuid = request.args.get('uuid')
    page = request.args.get('page')
    if page is None:
        page = 1
    page = 1 if int(page) < 1 else int(page)
    data = hb.get_photo_walls(uuid, page)
    template = '<head><title>%s</title></head>' % '精选照片'
    i = 0
    for item in data:
        if i % 2 == 0:
            template += "<div style='height=334px;'>"
        template += "<span style=\"width:48%%; %s\" onclick=\"location='%s'\"><img src='%s'></span>" % ('' if i % 2 == 0 else 'float:right;', item['src'], item['cover'])
        i = i + 1
        if i % 2 == 0:
            template += '</div>'

    # 上一页 下一页
    if page > 1:
        template = "<h2 style='text-align:center; color: blue' onclick=\"location='/snow_pack?uuid=%s&page=%s'\">上一页</h2>" % (uuid, page - 1) + template
    if len(data) >= 20:
        template = template + "<h2 style='text-align:center; color: green' onclick=\"location='/snow_pack?uuid=%s&page=%s'\">下一页</h2>" % (uuid, page + 1)

    return template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
