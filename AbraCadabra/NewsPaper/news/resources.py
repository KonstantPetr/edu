news = 'NW'
article = 'AR'

SECTION = [
    (news, 'Новость'),
    (article, 'Статья')]


class LikerMixIn:

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
