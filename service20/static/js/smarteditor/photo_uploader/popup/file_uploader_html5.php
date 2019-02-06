<?php

/*===============================================================
 �� �̹��� ������ ���� <�� - �Ϻμ��� >
 �� ȣ�� ���
 img_resize_gd(��������,���丮 ��ġ ���� ��������,�ִ���,�ִ����);
 ===============================================================*/
function fnImgResizeGD($file,$save_file,$max_width,$max_height){
	$img_info = getImageSize($file);		// img_info[0] : �̹��� width  1 : height   2 : type

	if($img_info[2] == 1){
		$src_img = ImageCreateFromGif($file);
	}elseif($img_info[2] == 2){
		$src_img = ImageCreateFromJPEG($file);
	}elseif($img_info[2] == 3){
		$src_img = ImageCreateFromPNG($file);
	}else{
		return 0;
	}

	//--------- ������ �ٽ� ���� ---------------
	if($img_info[0]<=$max_width){
		$re_width = $img_info[0];
		$re_height = $img_info[1];
	}else{
		$re_width = $max_width;
		$tmp = $img_info[0] - $max_width;
		$tmp2 = ceil($tmp / $img_info[0] * 100);
		$re_height = $img_info[1] - ($img_info[1] /100 * $tmp2);
	}


	if($img_info[2] == 1)$dst_img = imagecreate($re_width, $re_height);
	else $dst_img = imagecreatetruecolor($re_width, $re_height);
	$bgc = ImageColorAllocate($dst_img, 255, 255, 255);
	$srcx=0;
	$srcy=0;

	ImageCopyResampled($dst_img, $src_img, $srcx, $srcy, 0, 0, $re_width, $re_height, ImageSX($src_img),ImageSY($src_img));
		
	if($img_info[2] == 1){
		ImageInterlace($dst_img);
		ImageGif($dst_img, $save_file);
	}elseif($img_info[2] == 2){
		ImageInterlace($dst_img);
		ImageJPEG($dst_img, $save_file,100);
	}elseif($img_info[2] == 3){
		ImagePNG($dst_img, $save_file);
	}
	ImageDestroy($dst_img);
	ImageDestroy($src_img);
	////////// �̹��� ũ�� ��ȯ �� //////////////////
}

	/*-- ��� ���� �� ��� ���� --*/
	$updir = $_GET["updir"];	
	if($updir){
		$updir = "/_Data/" . $updir . "/" . date("Ym");
	}else{
		$updir = "/_Data/Editor" . "/" . date("Ym");
	}
	
	$t = explode("/" , $updir);
	$len = sizeof($t);
		
	for($k=1;$k<$len;$k++){
		$chkPath="";
		for($j=1;$j<=$k;$j++){
			if($chkPath)$chkPath.="/";
			if($t[$j])$chkPath.=$t[$j];
		}
		$chkPath = $_SERVER["DOCUMENT_ROOT"] . $chkPath;
	
		if(!is_dir($chkPath)){
			mkdir($chkPath, 0777);
			chmod($chkPath, 0777);
		}
	}
	$uploadDir = $chkPath . "/";
	
	
	
	/*-- ��� ���� �� ��� ���� �� --*/

 	$sFileInfo = '';
	$headers = array();
	 
	foreach($_SERVER as $k => $v) {if(substr($k, 0, 9) == "HTTP_FILE") {$k = substr(strtolower($k), 5);$headers[$k] = $v;}}
	
	$file = new stdClass;
	$file->name = str_replace("\0", "", rawurldecode($headers['file_name']));
	$file->size = $headers['file_size'];
	$file->content = file_get_contents("php://input");
	
	$filename_ext = strtolower(array_pop(explode('.',$file->name)));
	$allow_file = array("jpg", "png", "bmp", "gif"); 
	
	if(!in_array($filename_ext, $allow_file)) {
		echo "NOTALLOW_".$file->name;
	} else {
		
		//����Ǵ� ���� �̸� ����(�ߺ� ����)
		$exe = explode(".",$file->name);
		$len = sizeof($exe);
		$exe = $exe[$len-1];
		$nweFile = date(time()) . "." . $exe;
		// ���� �ߺ� üũ
		$cnt=0;
		while(file_exists($uploadDir . "/" . $nweFile)){
			$cnt++;
			$nweFile = date(time()) . "(" . $cnt .")." . $exe;
		}
		$newPath = $uploadDir.iconv("utf-8", "cp949", $nweFile);
		
		
		if(file_put_contents($newPath, $file->content)) {
			$sFileInfo .= "&bNewLine=true";
			$sFileInfo .= "&sFileName=".$nweFile;
			$sFileInfo .= "&sFileURL=".$updir ."/".$nweFile;
			
			//-- �̹��� ������ ���̱�
			fnImgResizeGD($newPath, $newPath,800,800);
		}
		
		echo $sFileInfo;
	}
?>