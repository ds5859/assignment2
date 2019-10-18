import unittest, requests
from bs4 import BeautifulSoup

server_address="http://127.0.0.1:5000"
server_login=server_address + "/login"
server_register=server_address + "/register"
server_spellcheck=server_address + "/spell_check"
#print("Test Ping Pages")
"""
def get_element_by_id(text, eid):
    soup = BeautifulSoup(text, "html.parser")
    result = soup.find(id=eid)
    return result

def login(uname, pword, twofactor, session=None):
    addr = server_login
    if session is None:
        session = requests.Session()
    test_creds = {"username": uname, "password": pword, "twofa": twofactor}
    r = session.post(addr, data = test_creds)
    print("h1")
    print("r")
    print("h2")
    success = get_element_by_id(r.text, 'result')
    assert success != None, "missing id='result' in your login response"
    return "success" in success.text
"""
class FeatureTest(unittest.TestCase):
    TESTING = True
    WTF_CSRF_ENABLED = False
    #check main page returns 200 OK
    def test_server_exists(self):
        response = requests.get(server_address)
        self.assertEqual(response.status_code, 200)
    #check login page returns 200 OK
    def test_login_page_exists(self):
        response = requests.get(server_login)
        self.assertEqual(response.status_code, 200)
    #check register page returns 200 OK
    def test_register_page_exists(self):
        response = requests.get(server_register)
        self.assertEqual(response.status_code, 200)
    #check spellcheck page returns 200 OK (note: unauthorized due to login requirement)
    def test_spellcheck_page_exists(self):
        response = requests.get(server_spellcheck)
        self.assertEqual(response.status_code, 200)
    """
    def test_login_bad_pass(self):
        res = self.get("/login")
        soup = BeautifulSoup(res.data, 'html.parser')
        csrf_token = soup.find('form').contents[1].attrs['value']
        res = self.post('/login',
                        data=dict(userName='user1', password='user1xyz', auth2fa='user1', csrf_token=csrf_token),
                        follow_redirects=True)
        soup = BeautifulSoup(res.data, 'html.parser')
        response = soup.find(id='result')
        assert (str(response.contents[0]) == 'Incorrect')
    
    def test_register(self):
        req = requests.post(url=server_register, data={'uname': 'BobTest', 'pword': 'Test1234', '2fa': '10001234567'})
        soup = BeautifulSoup(req.text, 'html.parser')
        msg = soup.find(id="success").text
        assert(msg =="success")
    """
    #check registration functionality 
    def test_register(self):
        sess=requests.session()
        response=sess.get(server_register)
        soup=BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())
        token=soup.find('input', {'name':'csrf_token'})['value']
        #print(token)

        post_data=('uname=%s&pword=%s&twofa=%s&csrf_token=%s' % ("TestUser1", "TestUser1", "10001234567", token))
        post_header={'Content-type': 'application/x-www-form-urlencoded'} #content type not working with multipart/form-data or text/plain
        response2=sess.post(url=server_register, headers=post_header, data=post_data)
        
        soup2=BeautifulSoup(response2.text, 'html.parser')
        #print(soupResult)
        result=soup2.find(id='success').text
        #print(soupAnswer)
        self.assertEqual(result, 'success')

    def test_register_existing_user(self):
        sess=requests.session()
        response=sess.get(server_register)
        soup=BeautifulSoup(response.text, 'html.parser')
        token=soup.find('input', {'name':'csrf_token'})['value']

        post_data=('uname=%s&pword=%s&twofa=%s&csrf_token=%s' % ("TestUser1", "TestUser1", "10001234567", token)) # make sure uname matches above test
        post_header={'Content-type': 'application/x-www-form-urlencoded'} 
        response2=sess.post(url=server_register, headers=post_header, data=post_data)
        
        soup2=BeautifulSoup(response2.text, 'html.parser')
        result=soup2.find(id='success').text
        self.assertEqual(result, 'failure')

    def test_invalid_login(self):
        sess=requests.session()
        response=sess.get(server_login)
        soup=BeautifulSoup(response.text, 'html.parser')
        token=soup.find('input', {'name':'csrf_token'})['value']
        
        post_data=('uname=%s&pword=%s&twofa=%s&csrf_token=%s' % ("TestUser50", "TestUser50", "10001234567", token)) # make sure uname not in dict or credentials mismatch
        post_header={'Content-type': 'application/x-www-form-urlencoded'} 
        response2=sess.post(url=server_login, headers=post_header, data=post_data)

        soup2=BeautifulSoup(response2.text, 'html.parser')
        result=soup2.find(id='result').text
        self.assertEqual(result, 'Incorrect')

    def test_valid_login(self):
        sess=requests.session()
        response=sess.get(server_login)
        soup=BeautifulSoup(response.text, 'html.parser')
        token=soup.find('input', {'name':'csrf_token'})['value']
        
        post_data=('uname=%s&pword=%s&twofa=%s&csrf_token=%s' % ("TestUser1", "TestUser1", "10001234567", token)) # make sure uname not in dict or credentials mismatch
        post_header={'Content-type': 'application/x-www-form-urlencoded'} 
        response2=sess.post(url=server_login, headers=post_header, data=post_data)

        soup2=BeautifulSoup(response2.text, 'html.parser')
        result=soup2.find(id='result').text
        self.assertEqual(result, 'Success')

    def test_spell_check(self): #must be logged in first
        sess=requests.session()
        response=sess.get(server_login)
        soup=BeautifulSoup(response.text, 'html.parser')
        token=soup.find('input', {'name':'csrf_token'})['value']
        
        post_data=('uname=%s&pword=%s&twofa=%s&csrf_token=%s' % ("TestUser1", "TestUser1", "10001234567", token)) # make sure uname not in dict or credentials mismatch
        post_header={'Content-type': 'application/x-www-form-urlencoded'} 
        response2=sess.post(url=server_login, headers=post_header, data=post_data)

        
        #sess=requests.session()
        response=sess.get(server_spellcheck)
        soup=BeautifulSoup(response.text, 'html.parser')
        #token=soup.find('input', {'name':'csrf_token'})['value']
        #print(token)
        
        spellinput="The quick broown faax jumped over the lazzy dog."
        post_data=('inputtext=%s&csrf_token=%s' % (spellinput, token)) #enter
        post_header={'Content-type': 'application/x-www-form-urlencoded'} 
        response2=sess.post(url=server_spellcheck, headers=post_header, data=post_data)

        soup2=BeautifulSoup(response2.text, 'html.parser')
        #print(soup2)
        #result=soup2.find('input', {'name':'misspelled'})['value']
        #print(result)
        result=soup2.find(id='misspelled').text
        print(result)
        result_fix=result.lstrip().strip()
        print(result_fix)
        #self.assertEqual (misspelled == "broown, faax, lazzy")

        #soup2=BeautifulSoup(response2.text, 'html.parser')
        #result=soup2.find(id='misspelled')
        #print(result)

        self.assertEqual(result_fix, 'broown, faax, lazzy')

    def test_debugger(self):
        response=requests.get(server_register)
        #print(response.status_code)
        #print(response.headers)
        soup=BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        links=soup.find_all("input")
        #print(links)
        #print(soup.p)
        