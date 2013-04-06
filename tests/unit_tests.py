from unittest import TestCase
from blast_sort import get_blast_dict


class BlastNoRegexTest(TestCase):
    def test_dna(self):
        blast_nos = {
            'gi|386767550|ref|NM_001259277.1|':'NM_001259277',
            'gi|269954741|gb|BT100316.1|':'BT100316',
            'gi|220947603|gb|FJ632086.1|':'FJ632086',
            'gi|3676166|emb|AJ011114.1|':'AJ011114',
            'gi|4689101|gb|AF073179.1|AF073179':'AF073179',
            'gi|349668|gb|L23195.1|DROCDHC64C':'L23195',
            'gi|627171|pir||A54148': 'A54148',
                }
        for blast_data in blast_nos:
            blast_dict = get_blast_dict(blast_data)
            print "Data: {0}".format(blast_data)
            self.assertEquals(blast_dict['blast'],
                    blast_nos[blast_data])

