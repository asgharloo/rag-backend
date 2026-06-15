--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-2.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-2.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_messages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    session_id uuid NOT NULL,
    sender character varying NOT NULL,
    content text NOT NULL,
    metadata_col jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.chat_messages OWNER TO postgres;

--
-- Name: chat_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_sessions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    client_id uuid NOT NULL,
    status character varying NOT NULL,
    summary text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    title character varying
);


ALTER TABLE public.chat_sessions OWNER TO postgres;

--
-- Name: client_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.client_profiles OWNER TO postgres;

--
-- Name: memories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memories (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    client_id uuid NOT NULL,
    session_id uuid,
    content text NOT NULL,
    embedding public.vector(1536) NOT NULL,
    emotion character varying(50),
    sentiment_score double precision,
    stress_level double precision,
    urgency_score double precision,
    memory_type character varying NOT NULL,
    importance_score double precision NOT NULL,
    decay_score double precision NOT NULL,
    metadata_col jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.memories OWNER TO postgres;

--
-- Name: specialist_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialist_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    specialization character varying(120) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.specialist_profiles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    role character varying NOT NULL,
    phone_number character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
626fad402c96
\.


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_messages (id, session_id, sender, content, metadata_col, created_at, updated_at) FROM stdin;
e125d0ba-4ac2-473d-83d5-2218757b60b1	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام .. خیلی داغون هستم 	\N	2026-06-13 13:37:13.233748+00	2026-06-13 13:37:13.233748+00
1ce62855-af06-4637-b0dd-b4e6e1106437	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 13:37:13.238576+00	2026-06-13 13:37:13.238576+00
7d156f49-0ee6-4fbb-9c0e-dae524c2446a	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام .. خیلی صص داغون هستم 	\N	2026-06-13 13:37:25.84738+00	2026-06-13 13:37:25.84738+00
c2bbf646-0782-4088-8c0b-325d24dc5664	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 13:37:25.850262+00	2026-06-13 13:37:25.850262+00
72fa2c41-d2de-4780-a4ba-0b6cb1852159	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام .. خیلی صص داغون هستم 	\N	2026-06-13 13:38:01.157818+00	2026-06-13 13:38:01.157818+00
4d8d5211-71de-4c8e-88bc-7b28fa6e4dc6	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 13:38:01.162591+00	2026-06-13 13:38:01.162591+00
a64292f4-edbb-49ad-9926-b97df165bb06	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام .. خیلی صص داغون هستم 	\N	2026-06-13 13:43:24.043423+00	2026-06-13 13:43:24.043423+00
03ba4b03-ef75-4976-8618-bcd0a05931d2	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 13:43:24.048208+00	2026-06-13 13:43:24.048208+00
53cd820d-f816-4aa5-aac8-3dfaaf968fca	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام ..ضضصضصضصض خیلی صص داغون هستم 	\N	2026-06-13 13:44:27.895865+00	2026-06-13 13:44:27.895865+00
5ec347b1-4f33-4e84-bcf2-65a298a307b9	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 13:44:27.899849+00	2026-06-13 13:44:27.899849+00
2232ccd1-5d0f-4981-b9c3-360954ef642c	7362599b-57b8-4492-9d6d-f0aa334a7838	user	سلام .ی صص کیری  هستم 	\N	2026-06-13 17:09:20.632652+00	2026-06-13 17:09:20.632652+00
9f3daa88-cc93-4037-8601-2dd95525caff	7362599b-57b8-4492-9d6d-f0aa334a7838	ai	This is a dummy response from the AI.	\N	2026-06-13 17:09:20.637904+00	2026-06-13 17:09:20.637904+00
104dcfde-dca3-4ec0-ab98-b270c0432fcf	44393543-f98b-4db6-b397-ecd7b9e036c7	user	سلام .ی صص کیری  هستم 	\N	2026-06-13 17:12:07.651009+00	2026-06-13 17:12:07.651009+00
48a2b795-0f5a-4c48-a0d3-367710be964a	44393543-f98b-4db6-b397-ecd7b9e036c7	ai	This is a dummy response from the AI.	\N	2026-06-13 17:12:07.652899+00	2026-06-13 17:12:07.652899+00
53d8b49c-d891-4b0b-b0d6-60307314a488	7ea97358-bddf-429b-92da-47d680a53bdd	user	شسیشسیشسسشیسیش هستم 	\N	2026-06-13 17:34:01.202905+00	2026-06-13 17:34:01.202905+00
565c15f3-3607-484e-b137-7a1a18f3d491	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:34:01.207961+00	2026-06-13 17:34:01.207961+00
4949cd3d-0a01-4918-8518-dd2d3bb64efd	7ea97358-bddf-429b-92da-47d680a53bdd	user	شسیشسیشسسشیسیش هستم 	\N	2026-06-13 17:49:20.298471+00	2026-06-13 17:49:20.298471+00
808202c3-d9e6-480b-af7a-dadae4a13644	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:49:20.303709+00	2026-06-13 17:49:20.303709+00
7d8b40ed-4b3a-4fb7-b683-0780c5f06b07	7ea97358-bddf-429b-92da-47d680a53bdd	user	string	\N	2026-06-13 17:49:46.550087+00	2026-06-13 17:49:46.550087+00
78fa00a8-22e1-4581-a0ee-f88ad80ecd97	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:49:46.554009+00	2026-06-13 17:49:46.554009+00
3f397ac9-ef50-430a-beb6-e04e2f2ec649	7ea97358-bddf-429b-92da-47d680a53bdd	user	شسیشسیسشیسش	\N	2026-06-13 17:56:40.047361+00	2026-06-13 17:56:40.047361+00
d92151f7-93a6-4fe6-b6ef-eeccd9753e8b	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:56:40.05231+00	2026-06-13 17:56:40.05231+00
fb5c7a6e-4302-4f03-bc4f-81c8e92a20c6	7ea97358-bddf-429b-92da-47d680a53bdd	user	111	\N	2026-06-13 17:56:45.746775+00	2026-06-13 17:56:45.746775+00
5dbae1b6-64f8-4c0b-9e5a-7271c642690a	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:56:45.751501+00	2026-06-13 17:56:45.751501+00
bb9ddd5a-e7f5-4241-8c9b-fe6c2a44bd9c	7ea97358-bddf-429b-92da-47d680a53bdd	user	222	\N	2026-06-13 17:56:56.720347+00	2026-06-13 17:56:56.720347+00
c7083331-0280-4884-be71-4e6bc5ee5690	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:56:56.724778+00	2026-06-13 17:56:56.724778+00
5d4764ca-d95d-48c0-97e2-4bb949e7c3ab	7ea97358-bddf-429b-92da-47d680a53bdd	user	333	\N	2026-06-13 17:57:04.993106+00	2026-06-13 17:57:04.993106+00
c0c8b768-a596-440e-b6d4-2ec2e60bcd83	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 17:57:04.995942+00	2026-06-13 17:57:04.995942+00
3c8144a1-e71a-4960-9494-a9aedda999b3	7ea97358-bddf-429b-92da-47d680a53bdd	user	444666	\N	2026-06-13 18:10:40.436317+00	2026-06-13 18:10:40.436317+00
c55b0867-84ca-491d-a919-e80594322c34	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 18:10:40.442294+00	2026-06-13 18:10:40.442294+00
1698f484-4e0a-4793-8cce-2e11cf769686	7ea97358-bddf-429b-92da-47d680a53bdd	user	7777745	\N	2026-06-13 18:11:00.917666+00	2026-06-13 18:11:00.917666+00
dd25077b-e789-441b-b46d-5706c5fde71f	7ea97358-bddf-429b-92da-47d680a53bdd	ai	This is a dummy response from the AI.	\N	2026-06-13 18:11:00.922055+00	2026-06-13 18:11:00.922055+00
6e9829e8-486f-49c7-8642-eb2582559c6f	d90920e9-eb73-41e4-96a2-9d32ceaebefa	client	ssssssg	\N	2026-06-14 08:08:31.043134+00	2026-06-14 08:08:31.043134+00
beac1a2a-6717-413b-8570-b27ffc781bfb	c058df74-d3b9-4bd2-9bef-b0174e666591	client	سشییسشی	\N	2026-06-14 09:34:58.973512+00	2026-06-14 09:34:58.973512+00
259ec3fc-5c81-4fb8-994f-51fb70b08bf1	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سشییسشی	\N	2026-06-14 10:33:28.773085+00	2026-06-14 10:33:28.773085+00
334d5b56-a07d-4b2b-a127-759a735f021a	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سشییسشی	\N	2026-06-14 10:34:05.424012+00	2026-06-14 10:34:05.424012+00
7c49199a-d305-476e-82a1-b51e0975049a	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سلام	\N	2026-06-14 14:05:43.381849+00	2026-06-14 14:05:43.381849+00
0dd3b754-2f05-4edb-987a-f4b875928a29	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سلام	\N	2026-06-14 14:17:42.444565+00	2026-06-14 14:17:42.444565+00
e231e4a5-f1f7-4f1b-b78a-f4fc8f124b30	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سلام	\N	2026-06-14 14:19:49.844312+00	2026-06-14 14:19:49.844312+00
ed50c0e1-6fc0-4594-80b0-5080647fde7e	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سلام	\N	2026-06-14 14:25:54.952929+00	2026-06-14 14:25:54.952929+00
13e035e0-f525-450a-9f1f-445672ae98b7	9f1ec270-bb04-408e-9d00-00b485c8be07	client	سلام	\N	2026-06-14 14:26:34.488438+00	2026-06-14 14:26:34.488438+00
32297551-131a-46f2-abf4-ad8c04e0aa4e	9f1ec270-bb04-408e-9d00-00b485c8be07	ai	سلام! چطور می‌توانم به شما کمک کنم؟	\N	2026-06-14 14:26:34.49328+00	2026-06-14 14:26:34.49328+00
e80c0fb2-cfaf-4979-85b9-500efff0ddbc	9f1ec270-bb04-408e-9d00-00b485c8be07	client	حالم خوب نیست	\N	2026-06-14 14:27:16.933899+00	2026-06-14 14:27:16.933899+00
e24ff630-5855-4065-94b9-a3459eaf0829	9f1ec270-bb04-408e-9d00-00b485c8be07	ai	متاسفم که این را می‌شنوم. گاهی اوقات روزهای سختی پیش می‌آید و احساس ناراحتی کاملاً طبیعی است.\n\nاگر دوست دارید، می‌توانید درباره چیزی که آزارتان می‌دهد صحبت کنید؛ گاهی فقط نوشتن و بیان احساسات می‌تواند کمی سبک‌تان کند. من اینجا هستم تا گوش دهم و بدون قضاوت با شما صحبت کنم.\n\nهمچنین اگر نمی‌خواهید درباره دلیل ناراحتی‌تان صحبت کنید، شاید انجام یک کار کوچک مثل نوشیدن یک لیوان آب، چند نفس عمیق کشیدن، یا گوش دادن به یک موسیقی آرام‌بخش، بتواند کمی حال‌وهوای شما را تغییر دهد.\n\nبه خودتان مهربان باشید. اگر نیاز به صحبت بیشتر دارید، من در خدمتم.	\N	2026-06-14 14:27:16.937077+00	2026-06-14 14:27:16.937077+00
61722e74-0906-4e15-ad69-4c0910fef05e	f99567d0-855d-4f59-8bd8-510994d79321	client	string	\N	2026-06-14 15:09:25.15075+00	2026-06-14 15:09:25.15075+00
b15f42d5-6c6d-4fb3-8bfe-0485db141635	f99567d0-855d-4f59-8bd8-510994d79321	ai	The term **"string"** has different meanings depending on the context. Here are the most common ones:\n\n### 1. In Computer Science & Programming\nA **string** is a sequence of characters used to represent text.\n\n- **Examples**:\n  - `"Hello, World!"`\n  - `"12345"`\n  - `"a"`\n\n- **Common Operations**:\n  - Concatenation: `"Hello" + " " + "World"` → `"Hello World"`\n  - Length: `len("abc")` → `3`\n  - Slicing: `"Python"[0:2]` → `"Py"`\n  - Searching: `"Hello".find("ell")` → `1`\n\n- **Languages**:\n  - Python: `s = "hello"`\n  - Java: `String s = "hello";`\n  - JavaScript: `let s = "hello";`\n  - C: `char s[] = "hello";`\n\n### 2. In Everyday Language\n- A **string** is a thin piece of cord or thread used for tying, hanging, or playing musical instruments.\n  - Example: "Tie the package with a string."\n  - Example: "Guitar strings"\n\n### 3. In Mathematics\n- A **string** can refer to a sequence of symbols in formal language theory (e.g., in automata or regular expressions).\n\n---\n\nWould you like help with:\n- String manipulation in a specific programming language?\n- Regular expressions?\n- Something else related to "strings"?\n\nLet me know! 😊	\N	2026-06-14 15:09:25.15608+00	2026-06-14 15:09:25.15608+00
8d7acac8-0ccd-452a-a897-820501631dd8	f99567d0-855d-4f59-8bd8-510994d79321	client	امروز با زنم داعوام شد 	\N	2026-06-14 15:10:06.053007+00	2026-06-14 15:10:06.053007+00
2a9a8414-c847-482d-85a9-07eb3b687926	f99567d0-855d-4f59-8bd8-510994d79321	ai	متاسفم که این اتفاق افتاده. دعوا در زندگی زناشویی می‌تواند بسیار کلافه‌کننده و دردناک باشد، اما به یاد داشته باشید که این یک مشکل **شایع** است و بسیاری از زوج‌ها با وجود اختلاف نظر، رابطه‌ای سالم و محبت‌آمیز دارند.\n\nبرای مدیریت این وضعیت و جلوگیری از آسیب بیشتر، چند پیشنهاد دوستانه دارم:\n\n### ۱. به خودتان و همسرتان فضا بدهید\nاگر هنوز هیجانات بالا است، سعی کنید مکالمه را متوقف کنید. عجله نکنید تا بلافاصله مشکل را حل کنید.\n*   به خودتان اجازه دهید چند ساعت آرام باشید تا خشم و استرس فروکش کند.\n*   گاهی اوقات سکوت موقت بهتر از حرف‌های تند و پشیمان‌کننده است.\n\n### ۲. ریشه دعوا را پیدا کنید\nمعمولاً دعواها به خاطر موضوع کوچک پیش نمی‌آیند.\n*   آیا این دعوا به خاطر همان موضوع خاص بود، یا خستگی، استرس کاری، یا مشکلات حل‌نشده قبلی باعث آن شده است؟\n*   گاهی اوقات "آخرین قطره" باعث فروپاشی می‌شود، نه خودِ موضوع فعلی.\n\n### ۳. از گفتگوی سازنده استفاده کنید\nوقتی هر دو آرام شدید، سعی کنید با هم صحبت کنید، اما با رعایت این نکات:\n*   **از "من" استفاده کنید، نه "تو"**: به جای گفتن "تو همیشه..." یا "تو هیچ‌وقت..."، بگویید "من احساس می‌کنم..." یا "من ناراحت شدم وقتی...". این کار باعث می‌شود طرف مقابل گارد نگیرد.\n*   **شنونده خوبی باشید**: اجازه دهید همسرتان حرفش را بزند بدون اینکه وسط حرفش بپرید یا دفاع کنید. فقط گوش دهید تا بفهمید او چه احساسی دارد.\n*   **به دنبال مقصر نگردید**: هدف برنده شدن در بحث نیست، بلکه درک متقابل و پیدا کردن راه‌حل است.\n\n### ۴. عذرخواهی کنید (اگر لازم است)\nحتی اگر فکر می‌کنید تقصیر اصلی با طرف مقابل است، عذرخواهی بابت **نحوه بیان حرف‌ها** یا **بلند صحبت کردن** می‌تواند یخ رابطه را آب کند. این به معنای تسلیم شدن نیست، بلکه به معنای ارزش قائل شدن برای رابطه است.\n\n### ۵. به دنبال راه‌حل باشید\nبعد از آرام شدن، با هم صحبت کنید که:\n*   چه چیزی باعث ناراحتی شما شد؟\n*   چگونه می‌توانیم از تکرار این دعوا در آینده جلوگیری کنیم؟\n\n---\n\n**نکته مهم:**\nاگر این دعواها مکرر هستند، خیلی شدید هستند، یا شامل توهین و خشونت کلامی/جسمی شده‌اند، حتماً از یک **مشاور خانواده** کمک بگیرید. مشاور می‌تواند ابزارهای ارتباطی بهتری به شما یاد بدهد.\n\nامروز سعی کنید یک کار کوچک و محبت‌آمیز انجام دهید (مثل خریدن خوراکی مورد علاقه‌اش، کمک در کارهای خانه، یا فقط یک پیام ساده برای ابراز نگرانی). این کارها می‌تواند پل ارتباطی را دوباره بسازد.\n\nآیا دوست دارید درباره موضوع خاصی از دعوا بیشتر صحبت کنیم؟	\N	2026-06-14 15:10:06.056317+00	2026-06-14 15:10:06.056317+00
26e2a2fe-b19b-443e-bb4a-a6f7f04c9e74	883c2bd8-9d62-4bb5-98c6-4556ca27d2f8	client	سلام.. بچه ام ناخن	\N	2026-06-15 10:53:21.857267+00	2026-06-15 10:53:21.857267+00
4ae13b92-82da-4efc-b198-27c91dd4edd0	883c2bd8-9d62-4bb5-98c6-4556ca27d2f8	ai	سلام! به نظر می‌رسد جمله شما ناتمام مانده است. لطفاً بفرمایید دقیقاً چه مشکلی برای ناخن کودک شما پیش آمده است؟\n\nآیا منظور شما یکی از موارد زیر است؟\n*   **جویدن ناخن؟**\n*   **لایه لایه شدن یا شکنندگی ناخن؟**\n*   **ضربه خوردن یا کبودی ناخن؟**\n*   **رشد غیرعادی یا قوز کردن ناخن؟**\n*   **مشکلات پوستی اطراف ناخن (مثل قرمزی یا چرک)؟**\n\nلطفاً جزئیات بیشتری بگویید تا بتوانم راهنمایی دقیق‌تری به شما ارائه دهم.	\N	2026-06-15 10:53:21.863199+00	2026-06-15 10:53:21.863199+00
\.


--
-- Data for Name: chat_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_sessions (id, client_id, status, summary, created_at, updated_at, title) FROM stdin;
0f51a8b2-9694-4084-9128-486675e28482	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-11 14:02:49.714387+00	2026-06-11 14:02:49.714387+00	session5
7ea97358-bddf-429b-92da-47d680a53bdd	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-11 15:01:40.577224+00	2026-06-11 15:01:40.577224+00	session5
ef50c913-808d-455f-8d14-94ba9c08a74b	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-11 15:10:16.478551+00	2026-06-11 15:10:16.478551+00	session5
7ce1e679-d061-4840-9d62-f96cf7f6d05a	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-11 15:12:21.054015+00	2026-06-11 15:12:21.054015+00	session5
a1d82c8e-ef9b-4b63-85a8-64e2d349a302	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-11 15:34:11.180401+00	2026-06-11 15:34:11.180401+00	session5
54862e8b-39fc-42e3-9401-182ae7e2ea62	a916b818-1c27-4e1e-a73c-be2c867b695c	active	\N	2026-06-13 09:53:04.261084+00	2026-06-13 09:53:04.261084+00	New Counseling Session2
faa11048-e944-4da3-acfd-5142c2752b27	a916b818-1c27-4e1e-a73c-be2c867b695c	active	\N	2026-06-13 10:11:27.886639+00	2026-06-13 10:11:27.886639+00	depression
8c0020de-c0ad-49e7-8921-d1d977bc4e09	a916b818-1c27-4e1e-a73c-be2c867b695c	active	\N	2026-06-13 11:07:12.532678+00	2026-06-13 11:07:12.532678+00	مشکل
0a848e9e-960d-40a7-8998-a6915581eed4	a916b818-1c27-4e1e-a73c-be2c867b695c	active	\N	2026-06-13 11:07:42.838675+00	2026-06-13 11:07:42.838675+00	 رررمشکل
d77149c7-3f73-4a4c-b235-0316252565ce	a916b818-1c27-4e1e-a73c-be2c867b695c	active	\N	2026-06-13 11:08:48.608542+00	2026-06-13 11:08:48.608542+00	22 رررمشکل
44393543-f98b-4db6-b397-ecd7b9e036c7	d5e3356e-7b75-4931-8fb8-ce916156dca3	active	\N	2026-06-13 13:00:55.212566+00	2026-06-13 13:00:55.212566+00	session3
10a25f26-5c2d-42fa-8192-45a5c44206db	d5e3356e-7b75-4931-8fb8-ce916156dca3	active	\N	2026-06-13 13:01:12.426124+00	2026-06-13 13:01:12.426124+00	گفتگوی جدید
7362599b-57b8-4492-9d6d-f0aa334a7838	d5e3356e-7b75-4931-8fb8-ce916156dca3	active	\N	2026-06-13 13:03:47.579216+00	2026-06-13 13:03:47.579216+00	گفتگوی جدید
1f399495-9af5-46b0-bfe4-5f3228434733	d5e3356e-7b75-4931-8fb8-ce916156dca3	active	\N	2026-06-13 17:10:27.112839+00	2026-06-13 17:10:27.112839+00	گفتگوی همسر
d8e70a1a-5ca9-4350-9ddf-fe028fb2d7be	1e5e840a-e150-4d88-a862-e1e4ae714b1a	active	\N	2026-06-14 08:06:47.54288+00	2026-06-14 08:06:47.54288+00	asdas
d90920e9-eb73-41e4-96a2-9d32ceaebefa	1e5e840a-e150-4d88-a862-e1e4ae714b1a	active	\N	2026-06-14 08:07:20.917959+00	2026-06-14 08:07:20.917959+00	گفتگوی جدید
c058df74-d3b9-4bd2-9bef-b0174e666591	0250ab8d-d351-4d24-824c-661710eb2fd2	active	\N	2026-06-14 09:33:47.357291+00	2026-06-14 09:33:47.357291+00	گفتگو 
9f1ec270-bb04-408e-9d00-00b485c8be07	0250ab8d-d351-4d24-824c-661710eb2fd2	active	\N	2026-06-14 10:32:47.479799+00	2026-06-14 10:32:47.479799+00	گفتشسیسشسشییسشیسشد
f99567d0-855d-4f59-8bd8-510994d79321	eece5bfd-5b6e-4ac0-88ea-b8b4b5f5d80f	active	\N	2026-06-14 15:08:32.560841+00	2026-06-14 15:08:32.560841+00	دعوا با همسر 
883c2bd8-9d62-4bb5-98c6-4556ca27d2f8	6c30e6a2-d656-407e-bbea-70530f78531a	active	\N	2026-06-15 10:52:38.20447+00	2026-06-15 10:52:38.20447+00	گناخن
\.


--
-- Data for Name: client_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client_profiles (id, user_id, first_name, last_name, created_at, updated_at) FROM stdin;
0c1684ad-1caa-4f6c-818f-0b78c2a15534	2340a430-ee41-40ce-bbd2-6fc98ca56a42	\N	\N	2026-06-10 17:51:49.328551+00	2026-06-10 17:51:49.328551+00
02ced874-cfd1-463e-b512-d89c840099da	640f54b4-9b1e-4a27-9066-1867e0bbf202	\N	\N	2026-06-11 10:41:55.549396+00	2026-06-11 10:41:55.549396+00
151f4865-57c0-4a89-9e0e-5dd0f8fc2c56	56fcfb58-c747-4593-af91-0d973ba0084f	\N	\N	2026-06-11 12:03:26.232634+00	2026-06-11 12:03:26.232634+00
bfd2efb0-88da-418c-95a6-e09e4f8888dd	f4a5b671-d871-4ab8-b4c5-6fc53d4bed74	\N	\N	2026-06-11 13:07:29.173137+00	2026-06-11 13:07:29.173137+00
6c30e6a2-d656-407e-bbea-70530f78531a	3890f1cf-241e-4139-b3e5-331fcea904dc	\N	\N	2026-06-11 13:23:11.086851+00	2026-06-11 13:23:11.086851+00
74c9f6fd-480d-4e9f-b7d5-663683aee41d	079dee2e-11c7-4c27-906e-b78f737c6e49	\N	\N	2026-06-11 15:38:59.245252+00	2026-06-11 15:38:59.245252+00
a916b818-1c27-4e1e-a73c-be2c867b695c	b3f42ad9-881a-43ea-b3c1-50ea22e516ff	\N	\N	2026-06-13 09:51:35.498171+00	2026-06-13 09:51:35.498171+00
d5e3356e-7b75-4931-8fb8-ce916156dca3	2900a0d1-b39c-4b09-9d2d-76d34a519a25	\N	\N	2026-06-13 11:23:50.390899+00	2026-06-13 11:23:50.390899+00
dacd40ac-dd23-457b-85f1-539ed1c0abdd	21282abb-a915-4d0b-ae80-d148e7370f87	\N	\N	2026-06-14 07:14:09.481981+00	2026-06-14 07:14:09.481981+00
1e5e840a-e150-4d88-a862-e1e4ae714b1a	d4ae6f17-71d8-4383-8718-8fefef65db3f	\N	\N	2026-06-14 07:33:36.092364+00	2026-06-14 07:33:36.092364+00
0250ab8d-d351-4d24-824c-661710eb2fd2	69a3e278-a2c6-4213-9aa4-061a43d9505f	\N	\N	2026-06-14 09:32:14.299043+00	2026-06-14 09:32:14.299043+00
eece5bfd-5b6e-4ac0-88ea-b8b4b5f5d80f	e6085998-95a1-4eb5-ab42-a0add0ab4f5f	\N	\N	2026-06-14 15:07:38.487759+00	2026-06-14 15:07:38.487759+00
\.


--
-- Data for Name: memories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memories (id, client_id, session_id, content, embedding, emotion, sentiment_score, stress_level, urgency_score, memory_type, importance_score, decay_score, metadata_col, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: specialist_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialist_profiles (id, user_id, specialization, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, role, phone_number, is_active, created_at, updated_at) FROM stdin;
2340a430-ee41-40ce-bbd2-6fc98ca56a42	client	09121010101	t	2026-06-10 17:51:49.328551+00	2026-06-10 17:51:49.328551+00
640f54b4-9b1e-4a27-9066-1867e0bbf202	client	09126060603	t	2026-06-11 10:41:55.549396+00	2026-06-11 10:41:55.549396+00
56fcfb58-c747-4593-af91-0d973ba0084f	client	09121010108	t	2026-06-11 12:03:26.232634+00	2026-06-11 12:03:26.232634+00
f4a5b671-d871-4ab8-b4c5-6fc53d4bed74	client	09126060601	t	2026-06-11 13:07:29.173137+00	2026-06-11 13:07:29.173137+00
3890f1cf-241e-4139-b3e5-331fcea904dc	client	09122222222	t	2026-06-11 13:23:11.086851+00	2026-06-11 13:23:11.086851+00
079dee2e-11c7-4c27-906e-b78f737c6e49	client	09484358669	t	2026-06-11 15:38:59.245252+00	2026-06-11 15:38:59.245252+00
b3f42ad9-881a-43ea-b3c1-50ea22e516ff	client	09121010103	t	2026-06-13 09:51:35.498171+00	2026-06-13 09:51:35.498171+00
2900a0d1-b39c-4b09-9d2d-76d34a519a25	client	09951435270	t	2026-06-13 11:23:50.390899+00	2026-06-13 11:23:50.390899+00
21282abb-a915-4d0b-ae80-d148e7370f87	client	09277676125	t	2026-06-14 07:14:09.481981+00	2026-06-14 07:14:09.481981+00
d4ae6f17-71d8-4383-8718-8fefef65db3f	client	09991759970	t	2026-06-14 07:33:36.092364+00	2026-06-14 07:33:36.092364+00
69a3e278-a2c6-4213-9aa4-061a43d9505f	client	09978341717	t	2026-06-14 09:32:14.299043+00	2026-06-14 09:32:14.299043+00
e6085998-95a1-4eb5-ab42-a0add0ab4f5f	client	09479776159	t	2026-06-14 15:07:38.487759+00	2026-06-14 15:07:38.487759+00
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: chat_sessions chat_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_sessions
    ADD CONSTRAINT chat_sessions_pkey PRIMARY KEY (id);


--
-- Name: client_profiles client_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_pkey PRIMARY KEY (id);


--
-- Name: client_profiles client_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_user_id_key UNIQUE (user_id);


--
-- Name: memories memories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_pkey PRIMARY KEY (id);


--
-- Name: specialist_profiles specialist_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialist_profiles
    ADD CONSTRAINT specialist_profiles_pkey PRIMARY KEY (id);


--
-- Name: specialist_profiles specialist_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialist_profiles
    ADD CONSTRAINT specialist_profiles_user_id_key UNIQUE (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_memory_embedding; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_memory_embedding ON public.memories USING hnsw (embedding public.vector_cosine_ops);


--
-- Name: ix_chat_messages_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_messages_session_id ON public.chat_messages USING btree (session_id);


--
-- Name: ix_chat_sessions_client_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_sessions_client_id ON public.chat_sessions USING btree (client_id);


--
-- Name: ix_memories_client_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memories_client_id ON public.memories USING btree (client_id);


--
-- Name: ix_memories_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_memories_session_id ON public.memories USING btree (session_id);


--
-- Name: ix_users_phone_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_phone_number ON public.users USING btree (phone_number);


--
-- Name: chat_messages chat_messages_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.chat_sessions(id) ON DELETE CASCADE;


--
-- Name: chat_sessions chat_sessions_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_sessions
    ADD CONSTRAINT chat_sessions_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client_profiles(id) ON DELETE CASCADE;


--
-- Name: client_profiles client_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: memories memories_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client_profiles(id) ON DELETE CASCADE;


--
-- Name: memories memories_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memories
    ADD CONSTRAINT memories_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.chat_sessions(id) ON DELETE CASCADE;


--
-- Name: specialist_profiles specialist_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialist_profiles
    ADD CONSTRAINT specialist_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

