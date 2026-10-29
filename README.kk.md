# AZIRAL Instagram Agent Skill

![AZIRAL Instagram Agent Skill](assets/cover.svg)

**Құрылтайшы мен өнім туралы контентке арналған бес дағды. Қазақша, орысша және ағылшынша.**

Расталған ақпараттан контент-жоспар, Reels сценарийі, пост мәтіні немесе карусель дайындаңыз. Жергілікті Python құралдарымен өз статистикаңызды талдаңыз. Әр тілдегі мәтіннің мағынасы мен деректері сақталуы керек.

[English](README.md) · [Русский](README.ru.md) · [MIT](LICENSE)

## Орнату

```sh
npx skills add azirali/instagram-agent-skill
```

Өзіңіз қолданатын агентті және орнату аясын таңдаңыз. Жеке дағдыны да орнатуға болады:

```sh
npx skills add azirali/instagram-agent-skill --skill aziral-instagram-reel
```

| Дағды | Нәтиже |
| --- | --- |
| `aziral-instagram-plan` | Ұстаным, расталған деректер және контент-жоспар |
| `aziral-instagram-reel` | Айтылатын мәтін, кадрлар жоспары және уақытты шамалау |
| `aziral-instagram-caption` | RU/EN/KK пост мәтіндері, alt text және мәтінді тексеру |
| `aziral-instagram-carousel` | Карусель немесе Stories тізбегі, визуал нұсқаулар |
| `aziral-instagram-insights` | CSV көрсеткіштерін әр формат ішінде салыстыру |

## Сұрау үлгісі

```text
$aziral-instagram-reel дағдысын қолдан. Қолданба прототипінің осы
жазбасынан 30 секундтық Reel жоспарын жаса. Бір әрекет пен оның
нәтижесін көрсет. Қазақша, орысша және ағылшынша жеке нұсқалар қажет.
Клиенттер, табыс немесе жетістіктер туралы ойдан дерек қоспа.
Алдымен кадрлар жоспары мен сөйлеу уақытын ұсын.
```

Жинақта автоматты жариялау интеграциясы жоқ. Дайындау үшін Instagram құпиясөзі, Meta API немесе ақылы сервис қажет емес. Қолданатын AI агентіңіздің өз тарифі болуы мүмкін. Видео жасау үшін құрал мен бастапқы материалдар бөлек қажет.

## Жергілікті құралдар

Python 3.10+ қажет, қосымша пакеттер орнатылмайды. Репозиторий түбірінен:

```sh
python3 skills/aziral-instagram-caption/scripts/caption_check.py examples/caption.kk.txt --language kk --strict
python3 skills/aziral-instagram-reel/scripts/beat_sheet.py examples/reel.kk.txt --wpm 145 --target 30
python3 skills/aziral-instagram-insights/scripts/insights.py examples/insights.csv
python3 -m unittest discover -s tests -v
```

Құралдар JSON шығарады, бастапқы файлды өзгертпейді және желіге сұрау жібермейді. Мәтін тексергіші emoji мен қазақ әріптерін сақтайды. Алдын ала көрініс Instagram экранының дәл көшірмесі емес. Сөйлеу уақыты шамамен есептеледі, оны дауыстап оқып тексеру керек.

Статистикада бос ұяшық белгісіз мәнді білдіреді, ал `0` - өлшенген нөл. Қамту нөл немесе белгісіз болса, коэффициент `null` болады. Қаралымдар сол форматтағы берілген іріктеменің медианасымен салыстырылады, оған қарастырылатын пост та кіреді. Бұл талдау болашақ танымалдықты болжамайды.

[CSV үлгісі](examples/insights.csv) - синтетикалық тест деректері, AZIRAL аккаунтының нәтижелері емес. [Мәтін үлгілері](examples) жинақтың мүмкіндіктерін көрсетеді, дайын видео немесе сурет болып саналмайды.

## Unicode тексеру мысалдары

[20 мысалдан тұратын жинақ](examples/unicode-regression) RU/EN/KK мәтінін, joiner бар emoji, біріктірілетін екпін белгілерін, жалауларды, модификаторларды және жол ауыстыруды қамтиды. Жергілікті Python және JavaScript тексерулері өлшем бірліктері мен орта нұсқаларын көрсетеді. Joiner жоғалса немесе байт саны өзгерсе, тексеру қатені табады және бастапқы мәтінді өзгертпейді. Бұл Unicode сәйкестігінің толық сынағы емес, шағын регрессиялық жинақ.

```sh
python3 examples/unicode-regression/verify.py
node examples/unicode-regression/verify.mjs
```

[Олжас Азирали / AZIRAL ұсынған тегін браузер құралы](https://aziral.com/kk/tools/unicode-text-checker) өз мәтініңізді тексеруге арналған. Репозиторийдегі жинақ мысалдарды жергілікті ортада қайталауға көмектеседі.

## Демо және талдау

[36 секундтық дыбыссыз демо](https://aziral.com/media/instagram-agent-skill/demo.mp4) және [тік форматтағы нұсқа](https://aziral.com/media/instagram-agent-skill/demo-vertical.mp4) CLI құралдарының нақты нәтижелерін көрсетеді. Анимация AI көмегімен дайындалды; статистика деректері синтетикалық, сөйлеу уақыты шамамен есептеледі.

- [Олжас Азиралидің талдауы (орысша)](https://aziral.com/blog/instagram-agent-skill-aziral-unicode-ru-en-kk)
- [Medium техникалық мақаласы (ағылшынша)](https://medium.com/@olzasazirali/unicode-safe-content-tools-for-english-russian-and-kazakh-769024c567f3)

## Автор және лицензия

**Олжас Азирали / AZIRAL** жасаған дербес жұмыс. [MIT лицензиясы](LICENSE).
Идеяға [Jake Schincariol жобасы](https://github.com/Jakeschincariol/instagram-agent-skill) шабыт берді. Оның файлдары, формулалары және зерттеу нәтижелері жинаққа кірмейді. Толығырақ: [NOTICE.md](NOTICE.md). Жоба бастапқы авторға, Instagram немесе Meta компанияларына қатысы жоқ және олардың мақұлдауын білдірмейді.

[AZIRAL](https://aziral.com) · [Олжас Азирали](https://aziral.com/olzhas-azirali)

Жинақ пайдалы болса, жұлдызша оны басқа адамдардың табуына көмектеседі.

