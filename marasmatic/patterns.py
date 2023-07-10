from .Expression import Expression



PunctuationMark = Expression(r'-|—|\.|,|\?|!')
Word            = Expression(r'(?:й|ц|у|к|е|н|г|ш|щ|з|х|ф|ы|в|а|п|р|о|л|д|ж|э|я|ч|с|м|и|т|ь|б|ю|ъ|ё|)+')