<!--#include virtual="..\..\lms.common\_system\system.asp"-->
<%	
Set objUp = Server.CreateObject("SiteGalaxyUpload.Form") '// ���ô� ���Ͼ��ε� ������Ʈ�� ���� 
'objUp.AbsolutePath = True 
attach_file1 = objUp("Filedata")
sFileInfo = fileup(attach_file1,"smartEditor")
sFile = replace(sFileInfo(1),"\","/")

Dim qimg, callback_func, f_name, f_url 
callback_func = objUp("callback_func") '// �˾�â�� �����ϴ� iframe �̸� �Դϴ�. �� ���� �״�� �޾Ƽ� �״�� �ѱ�ϴ�. 

   '// ���� ���ε� �κ��� ���ô� ������Ʈ�� ��ȯ�濡 ���� �ٸ� �� �ֽ��ϴ�. 
    IF trim(sFile) <> "" THEN     				
		   f_url = "http://" & DataUrl & "/" & DataFolder & "/"&sFile '// �̹��� URL 
    END If 
    
    '// �̺κ��� �߿��մϴ�. 
    '// ���Ͼ��ε� ó���ϰ� ���� callback.html�� ���ε�� ���� ������ �Ѱ��ݴϴ�. 
    '// callback_func �� ������ ������ȵ��� iframe�̸��ε� �޾Ƽ� �״�� �Ѱ��ݴϴ�. 
    '// bNewLine=true �� ���� �������� true�� �Ѱ��ָ� �����Ϳ��� �̹����� �ٰ� �̹��� ������ Ŀ���� �����ٴ� ���ε� �մϴ�. 
    '// sFileName �� �̹��� ���ϸ� 
    '// sFileURL �� �̹��� URL 

        response.redirect "/common/smarteditor/popup/quick_photo/callback.html?callback_func="&callback_func&"&bNewLine=true&sFileName="&f_name&"&sFileURL="&f_url 
        '--> ����Ʈ ������ ���, ./se2/~~~~ �� �Ϲ����Դϴ�. 
 %> 