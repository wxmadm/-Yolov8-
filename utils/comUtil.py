import uuid

class ComUtil:
    @classmethod
    def zh_ch(cls,string):
        return string.encode("gbk").decode(errors="ignore")

    @classmethod
    def uuid(cls):
        return uuid.uuid4().hex.replace("-","")