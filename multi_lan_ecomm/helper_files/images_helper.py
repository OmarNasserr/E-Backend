class Images_Helper():
    
    supported_formats=['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.svg','.SVG']
    
    def validate_image(image_name):
        
        if not any([True if image_name.endswith(i) else False for i in Images_Helper.supported_formats]):
            return False
        else:
            return True
