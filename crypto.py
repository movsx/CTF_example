# -*- coding: utf-8 -*-
import sys
### Merkle–Hellman knapsack cryptosystem
# условие
"""
def generate_public_key(private_key):
	n = 199285318978668966527551342512997250816637709274749259983292077699440369
	t = 32416190071
	return list(map(lambda x: (t * x) % n, private_key))

def crypt(open_text, public_key):
	bts = []
	[bts.extend([int(b) for b in '00000000'[len(bin(ord(c))[2:]):] + bin(ord(c))[2:]]) for c in open_text]
	return [sum(map(lambda x: x[0] * x[1] ,zip(blk, public_key))) for blk in [bts[i * 128:(i+1) * 128] for i in range(len(open_text) // 16)]]

public_key = [1050809378719198985041, 2101618757438397970082, 6304856272315193910246, 18914568816945581730738, 56743706450836745192214, 170231119352510235576642, 510693358057530706729926, 1532080074172592120189778, 4596240222517776360569334, 13788720667553329081708002, 41366162002659987245124006, 124098486007979961735372018, 372295458023939885206116054, 1116886374071819655618348162, 3350659122215458966855044486, 10051977366646376900565133458, 30155932099939130701695400374, 90467796299817392105086201122, 271403388899452176315258603366, 814210166698356528945775810098, 2442630500095069586837327430294, 7327891500285208760511982290882, 21983674500855626281535946872646, 65951023502566878844607840617938, 197853070507700636533823521853814, 593559211523101909601470565561442, 1780677634569305728804411696684326, 5342032903707917186413235090052978, 16026098711123751559239705270158934, 48078296133371254677719115810476802, 144234888400113764033157347431430406, 432704665200341292099472042294291218, 1298113995601023876298416126882873654, 3894341986803071628895248380648620962, 11683025960409214886685745141945862886, 35049077881227644660057235425837588658, 105147233643682933980171706277512765974, 315441700931048801940515118832538297922, 946325102793146405821545356497614893766, 2838975308379439217464636069492844681298, 8516925925138317652393908208478534043894, 25550777775414952957181724625435602131682, 76652333326244858871545173876306806395046, 229956999978734576614635521628920419185138, 689870999936203729843906564886761257555414, 2069612999808611189531719694660283772666242, 6208838999425833568595159083980851317998726, 18626516998277500705785477251942553953996178, 55879550994832502117356431755827661861988534, 167638652984497506352069295267482985585965602, 502915958953492519056207885802448956757896806, 1508747876860477557168623657407346870273690418, 4526243630581432671505870972222040610821071254, 13578730891744298014517612916666121832463213762, 40736192675232894043552838749998365497389641286, 122208578025698682130658516249995096492168923858, 366625734077096046391975548749985289476506771574, 1099877202231288139175926646249955868429520314722, 3299631606693864417527779938749867605288560944166, 9898894820081593252583339816249602815865682832498, 29696684460244779757750019448748808447597048497494, 89090053380734339273250058346246425342791145492482, 267270160142203017819750175038739276028373436477446, 801810480426609053459250525116217828085120309432338, 2405431441279827160377751575348653484255360928297014, 7216294323839481481133254726045960452766082784891042, 21648882971518444443399764178137881358298248354673126, 64946648914555333330199292534413644074894745064019378, 194839946743665999990597877603240932224684235192058134, 584519840230997999971793632809722796674052705576174402, 1753559520692993999915380898429168390022158116728523206, 5260678562078981999746142695287505170066474350185569618, 15782035686236945999238428085862515510199423050556708854, 47346107058710837997715284257587546530598269151670126562, 142038321176132513993145852772762639591794807455010379686, 426114963528397541979437558318287918775384422365031139058, 1278344890585192625938312674954863756326153267095093417174, 3835034671755577877814938024864591268978459801285280251522, 11505104015266733633444814074593773806935379403855840754566, 34515312045800200900334442223781321420806138211567522263698, 103545936137400602701003326671343964262418414634702566791094, 310637808412201808103009980014031892787255243904107700373282, 931913425236605424309029940042095678361765731712323101119846, 2795740275709816272927089820126287035085297195136969303359538, 8387220827129448818781269460378861105255891585410907910078614, 25161662481388346456343808381136583315767674756232723730235842, 75484987444165039369031425143409749947303024268698171190707526, 226454962332495118107094275430229249841909072806094513572122578, 679364886997485354321282826290687749525727218418283540716367734, 2038094660992456062963848478872063248577181655254850622149103202, 6114283982977368188891545436616189745731544965764551866447309606, 18342851948932104566674636309848569237194634897293655599341928818, 55028555846796313700023908929545707711583904691880966798025786454, 165085667540388941100071726788637123134751714075642900394077359362, 495257002621166823300215180365911369404255142226928701182232078086, 1485771007863500469900645541097734108212765426680786103546696234258, 4457313023590501409701936623293202324638296280042358310640088702774, 13371939070771504229105809869879606973914888840127074931920266108322, 40115817212314512687317429609638820921744666520381224795760798324966, 120347451636943538061952288828916462765233999561143674387282394974898, 361042354910830614185856866486749388295701998683431023161847184924694, 1083127064732491842557570599460248164887105996050293069485541554774082, 3249381194197475527672711798380744494661317988150879208456624664322246, 9748143582592426583018135395142233483983953964452637625369873992966738, 29244430747777279749054406185426700451951861893357912876109621978900214, 87733292243331839247163218556280101355855585680073738628328865936700642, 63914557751326551213938313155843053250929047765471955901694520110661557, 191743673253979653641814939467529159752787143296415867705083560331984671, 176660381804601027870342133376592977625086011339749083148666525597073275, 131410507456465150555923715103784431241982615469748729479415421392339087, 194946203390726485140219802798356042909310137134496928454954186477576892, 186267972214841522365556723369073627094654992853992265398278404033849938, 160233278687186634041567485081226379650689560012478276228251056702669076, 82129198104221969069599770217684637318793261487936308718169014709126490, 47102275333996940681247968140056661139742075189059666171214966427939101, 141306826001990822043743904420169983419226225567178998513644899283817303, 25349840048634533076129028234515448624403258152038475574350542452571171, 76049520145903599228387084703546345873209774456115426723051627357713513, 28863241459041831157609911597641786802991614093597020185862804373700170, 86589724377125493472829734792925360408974842280791060557588413121100510, 60483854152707513890937861865778830410286817567623921689473161663861161, 181451562458122541672813585597336491230860452702871765068419484991583483, 145784049417029691963338071766014972059305939559116775238674299575869711, 38781510293751142834911530272050414544642400127851805749438743328728395, 116344530881253428504734590816151243633927200383555417248316229986185185, 149748273665091318986652429935456480085143891875916991761656612259115186, 50674183037936023904854604780374938622156257078252455318385681378464820, 152022549113808071714563814341124815866468771234757365955157044135394460]
cipher_text =
	[
		1387977778999926469357780220487630125151962348185941993910077394771302677,
		1192236960845781949613172279312582839292898077268409678421304772227241438,
		1295152741157953792099179799985052248167548374589648818528421499250916999,
		828724787424187908000366458781164595076558885463707900320215679908512646,
		1179926879709109047038661681316962368287877340885819899201698611790531134,
		965171312356484716595815857561729919489896088681139239093293829323154838,
		1099367377207651843612375443021502714028353049437532392256489525051038347,
		1374891605015623267623322424512489936836885983493815443812918444687247914,
		1152880248428103510879661300981452627677389745079857275081612568623556291,
		962409003220820525413536841942678826309419979028794415812582008820263317
	]
"""
# решение 1
def Merkle():
    n = 199285318978668966527551342512997250816637709274749259983292077699440369
    t = 32416190071
    public_key = [ 1050809378719198985041, 2101618757438397970082, 6304856272315193910246, 18914568816945581730738, 56743706450836745192214, 170231119352510235576642, 510693358057530706729926, 1532080074172592120189778, 4596240222517776360569334, 13788720667553329081708002, 41366162002659987245124006, 124098486007979961735372018, 372295458023939885206116054, 1116886374071819655618348162, 3350659122215458966855044486, 10051977366646376900565133458, 30155932099939130701695400374, 90467796299817392105086201122, 271403388899452176315258603366, 814210166698356528945775810098, 2442630500095069586837327430294, 7327891500285208760511982290882, 21983674500855626281535946872646, 65951023502566878844607840617938, 197853070507700636533823521853814, 593559211523101909601470565561442, 1780677634569305728804411696684326, 5342032903707917186413235090052978, 16026098711123751559239705270158934, 48078296133371254677719115810476802, 144234888400113764033157347431430406, 432704665200341292099472042294291218, 1298113995601023876298416126882873654, 3894341986803071628895248380648620962, 11683025960409214886685745141945862886, 35049077881227644660057235425837588658, 105147233643682933980171706277512765974, 315441700931048801940515118832538297922, 946325102793146405821545356497614893766, 2838975308379439217464636069492844681298, 8516925925138317652393908208478534043894, 25550777775414952957181724625435602131682, 76652333326244858871545173876306806395046, 229956999978734576614635521628920419185138, 689870999936203729843906564886761257555414, 2069612999808611189531719694660283772666242, 6208838999425833568595159083980851317998726, 18626516998277500705785477251942553953996178, 55879550994832502117356431755827661861988534, 167638652984497506352069295267482985585965602, 502915958953492519056207885802448956757896806, 1508747876860477557168623657407346870273690418, 4526243630581432671505870972222040610821071254, 13578730891744298014517612916666121832463213762, 40736192675232894043552838749998365497389641286, 122208578025698682130658516249995096492168923858, 366625734077096046391975548749985289476506771574, 1099877202231288139175926646249955868429520314722, 3299631606693864417527779938749867605288560944166, 9898894820081593252583339816249602815865682832498, 29696684460244779757750019448748808447597048497494, 89090053380734339273250058346246425342791145492482, 267270160142203017819750175038739276028373436477446, 801810480426609053459250525116217828085120309432338, 2405431441279827160377751575348653484255360928297014, 7216294323839481481133254726045960452766082784891042, 21648882971518444443399764178137881358298248354673126, 64946648914555333330199292534413644074894745064019378, 194839946743665999990597877603240932224684235192058134, 584519840230997999971793632809722796674052705576174402, 1753559520692993999915380898429168390022158116728523206, 5260678562078981999746142695287505170066474350185569618, 15782035686236945999238428085862515510199423050556708854, 47346107058710837997715284257587546530598269151670126562, 142038321176132513993145852772762639591794807455010379686, 426114963528397541979437558318287918775384422365031139058, 1278344890585192625938312674954863756326153267095093417174, 3835034671755577877814938024864591268978459801285280251522, 11505104015266733633444814074593773806935379403855840754566, 34515312045800200900334442223781321420806138211567522263698, 103545936137400602701003326671343964262418414634702566791094, 310637808412201808103009980014031892787255243904107700373282, 931913425236605424309029940042095678361765731712323101119846, 2795740275709816272927089820126287035085297195136969303359538, 8387220827129448818781269460378861105255891585410907910078614, 25161662481388346456343808381136583315767674756232723730235842, 75484987444165039369031425143409749947303024268698171190707526, 226454962332495118107094275430229249841909072806094513572122578, 679364886997485354321282826290687749525727218418283540716367734, 2038094660992456062963848478872063248577181655254850622149103202, 6114283982977368188891545436616189745731544965764551866447309606, 18342851948932104566674636309848569237194634897293655599341928818, 55028555846796313700023908929545707711583904691880966798025786454, 165085667540388941100071726788637123134751714075642900394077359362, 495257002621166823300215180365911369404255142226928701182232078086, 1485771007863500469900645541097734108212765426680786103546696234258, 4457313023590501409701936623293202324638296280042358310640088702774, 13371939070771504229105809869879606973914888840127074931920266108322, 40115817212314512687317429609638820921744666520381224795760798324966, 120347451636943538061952288828916462765233999561143674387282394974898, 361042354910830614185856866486749388295701998683431023161847184924694, 1083127064732491842557570599460248164887105996050293069485541554774082, 3249381194197475527672711798380744494661317988150879208456624664322246, 9748143582592426583018135395142233483983953964452637625369873992966738, 29244430747777279749054406185426700451951861893357912876109621978900214, 87733292243331839247163218556280101355855585680073738628328865936700642, 63914557751326551213938313155843053250929047765471955901694520110661557, 191743673253979653641814939467529159752787143296415867705083560331984671, 176660381804601027870342133376592977625086011339749083148666525597073275, 131410507456465150555923715103784431241982615469748729479415421392339087, 194946203390726485140219802798356042909310137134496928454954186477576892, 186267972214841522365556723369073627094654992853992265398278404033849938, 160233278687186634041567485081226379650689560012478276228251056702669076, 82129198104221969069599770217684637318793261487936308718169014709126490, 47102275333996940681247968140056661139742075189059666171214966427939101, 141306826001990822043743904420169983419226225567178998513644899283817303, 25349840048634533076129028234515448624403258152038475574350542452571171, 76049520145903599228387084703546345873209774456115426723051627357713513, 28863241459041831157609911597641786802991614093597020185862804373700170, 86589724377125493472829734792925360408974842280791060557588413121100510, 60483854152707513890937861865778830410286817567623921689473161663861161, 181451562458122541672813585597336491230860452702871765068419484991583483, 145784049417029691963338071766014972059305939559116775238674299575869711, 38781510293751142834911530272050414544642400127851805749438743328728395, 116344530881253428504734590816151243633927200383555417248316229986185185, 149748273665091318986652429935456480085143891875916991761656612259115186, 50674183037936023904854604780374938622156257078252455318385681378464820, 152022549113808071714563814341124815866468771234757365955157044135394460 ]
    cipher_text = [ 1387977778999926469357780220487630125151962348185941993910077394771302677, 1192236960845781949613172279312582839292898077268409678421304772227241438, 1295152741157953792099179799985052248167548374589648818528421499250916999, 828724787424187908000366458781164595076558885463707900320215679908512646, 1179926879709109047038661681316962368287877340885819899201698611790531134, 965171312356484716595815857561729919489896088681139239093293829323154838, 1099367377207651843612375443021502714028353049437532392256489525051038347, 1374891605015623267623322424512489936836885983493815443812918444687247914, 1152880248428103510879661300981452627677389745079857275081612568623556291, 962409003220820525413536841942678826309419979028794415812582008820263317 ]
    private_key = [ t ] + [ t * 2 * 3 ** i for i in xrange( 0, 127 ) ]
    t2inv = 113733348753781020783170490400630827179237386517084745662682984487937812

    def dec( block ):
        r = ''
        ohlol = t2inv * block % n
        if ohlol % 2 == 1:
            r += '1'
            ohlol -= 1
        ohlol /= 2
        for i in xrange( 1, 128 ):
            r += '%s' % (ohlol % 3 ** i / 3 ** (i - 1))
        return hex( int( r, 2 ) )[ 2: ].rstrip( 'L' ).decode( 'hex' )

    for c in cipher_text:
        try:
            sys.stdout.write( dec( c ) )
        except:
            print 'FAIL'

# решение 2
"""
This is what we got when analysing the public_key list:

    sage: factor(1050809378719198985041)
    32416190071^2
    sage: factor(2101618757438397970082)
    2 * 32416190071^2
    sage: factor(6304856272315193910246)
    2 * 3 * 32416190071^2
    sage: factor(18914568816945581730738)
    2 * 3^2 * 32416190071^2
    sage: factor(56743706450836745192214)
    2 * 3^3 * 32416190071^2
    sage: factor(170231119352510235576642)
    2 * 3^4 * 32416190071^2

Looks like the private_key is generated based on the given 't' value. This is how we generated the private_key list

    private_key = [t]
    for i in range(0,127):
        private_key.append(2 * 3**i * t)

The generated private keys can be verified using the given generate_public_key() function. We got a match. Then we wrote the routine for inverse knapsack sum to get the flag. Here is the final code:
"""
def Merkle2():
    n = 199285318978668966527551342512997250816637709274749259983292077699440369
    t = 32416190071
    t_inv = 3607086840002694423309872675805192458275553329397325526691156370525160 #sage: inverse_mod(t,n)

    private_key = [t]
    for i in range(0,127):
        private_key.append(2 * 3**i * t)

    cipher_text = [
      1387977778999926469357780220487630125151962348185941993910077394771302677,
      1192236960845781949613172279312582839292898077268409678421304772227241438,
      1295152741157953792099179799985052248167548374589648818528421499250916999,
      828724787424187908000366458781164595076558885463707900320215679908512646,
      1179926879709109047038661681316962368287877340885819899201698611790531134,
      965171312356484716595815857561729919489896088681139239093293829323154838,
      1099367377207651843612375443021502714028353049437532392256489525051038347,
      1374891605015623267623322424512489936836885983493815443812918444687247914,
      1152880248428103510879661300981452627677389745079857275081612568623556291,
      962409003220820525413536841942678826309419979028794415812582008820263317
           ]

    def decrypt(cipher, private_key):   # inverse knapsack

        bts = ['0']*128                 # generate bit string
        for i in range(len(private_key) - 1, -1, -1):
            if cipher >= private_key[i]:
                bts[i] = '1'
                cipher = cipher - private_key[i]

        for j in range(0,128,8):        # generate chars out of every 8-bits
            sys.stdout.write(chr(int(''.join(bts[j:j+8]),2)))

    for c in cipher_text:               # iterate through 10 blocks
        decrypt((c * t_inv) % n,private_key)
    print ''


### Пример взлома RSA методом факторизации Ферма на основе того, что в задаче p и q расположены близко друг к другу
# Ссылка на метод факторизации Ферма http://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D1%84%D0%B0%D0%BA%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%A4%D0%B5%D1%80%D0%BC%D0%B0
### Условие
# n = 52663327194823108047941861363554667296911056447871 88785127198792390818389767437741043884042697813417 40858276714053716810874389770623503703996736687974 70776186113807376857893834326388369431932515506157 59902933749676883316817097953054649047764645797986 77703632934375663507898357576891627341435121532539 03202593
# e = 10662335266334707061416010175090707752184800780484 87199510272395686606199019585683070878871806968902 65830636660853997681894517472390188901902543758517 09269
# cipher-text = 10462822375277205946365199641597262713749993739943 57909091506537398272791306618098458481620423392938 70744463265888874276961969971096108086452105647668 82647584743088857818448828460464362997716024535291 28094029803725929915632320170106381959701908835246 76285475884921692502194212799981792187650488093680 64725175
### Решение
# Since python's float->int casting is inaccurate, I used SAGE.
# An actual s=(p-q)/2 value was obtained from the very first iteration:
### Код:
# sage: r=ceil(sqrt(n))
# sage: t=r+0 #first iteration
# sage: s=sqrt(t**2-n)
# sage: s #should be integer
# 1754844
# sage: p=t-s
# sage: q=t+s
#sage: phi=(p-1)*(q-1)
# sage: d=pow(e,-1,phi)
# sage: pow(c,d,n)
# 22424170465
### The flag is 22424170465

Merkle()
print
Merkle2()