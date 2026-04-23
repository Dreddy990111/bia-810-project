# Atelier — Vendor Intelligence Platform
## BIA 810 Final Presentation Script
### Team: Dhanvanth Reddy, Rohini Mallikarjunaiah, Jaanvi Vemana, Lynn Chirimumimba

**Total target time: 15 minutes**
**Speaking pace: ~130–140 words per minute**

---

---

## DHANVANTH — Introduction & Problem Statement
### Target time: 3.5 minutes (~460 words)

---

Good afternoon, everyone. I'm Dhanvanth, and on behalf of our team — Rohini, Jaanvi, and Lynn — thank you for having us.

I want to start with a scenario. Imagine you're planning a corporate dinner for 200 guests in New York City. You need a venue, a catering company, and AV equipment. Where do you even start? You Google "corporate catering NYC," open twelve tabs, compare PDFs, email five vendors for quotes, wait days for responses — and by the time you have enough information to make a decision, you've spent more time researching vendors than actually planning the event.

This is the problem we set out to solve.

Event planning is a 330-billion-dollar global industry, and yet the vendor discovery process still feels like it's stuck in 2005. It's fragmented. It's time-consuming. And it's almost entirely dependent on personal networks or blind Google searches. There's no intelligent, centralized platform that helps you find the right vendor for your specific event context — your budget, your event type, your guest count, your neighborhood.

And this is exactly where generative AI changes the game.

In this course, we've been asked to think about how large language models and AI tools can solve real business problems — not just automate tasks, but create genuine value for users. We took that challenge seriously. We asked ourselves: what would an AI-first approach to vendor discovery actually look like? Not just a search bar with better keywords, but a system that understands context, makes recommendations, and lets you have a conversation with your data.

The answer is Atelier.

Atelier is a vendor intelligence platform built for event planners. It aggregates 125 vendors across venues, catering companies, and AV providers in the New York metro area. It filters and ranks them intelligently based on your event context. And it lets you ask natural language questions — things like "show me catering options under $5,000 for a wedding" or "which venues in Manhattan have the highest ratings for corporate events?" — and get real, grounded answers from our dataset.

We built this end-to-end: a deployed web application, running live in production on Cloudflare's global edge network, powered by Anthropic's Claude model. This is not a mockup. This is not a wireframe. You can log in and use it right now.

Let me hand it over to Rohini, who is going to walk you through exactly what Atelier does and how it's built.

---
*[Transition: Dhanvanth gestures to Rohini]*

---

---

## ROHINI — Solution & Platform Features
### Target time: 3.5 minutes (~460 words)

---

Thank you, Dhanvanth. Hi everyone, I'm Rohini.

So — what does Atelier actually do? Let me break it down.

The core problem with vendor discovery isn't just that information is scattered. It's that comparing vendors is apples-to-oranges. A catering company quotes you per person. A venue quotes you a flat rental fee. An AV company quotes you hourly. There's no common language, no standard format, no easy way to compare.

Atelier solves that by doing the translation for you.

We pulled real pricing data from an event vendor dataset — 125 vendors, three categories — and we normalized everything so you can actually compare. Catering prices are shown per person. AV costs are broken out hourly. Venue prices show the total midpoint based on real market data. Apples to apples.

On top of that pricing foundation, we built three layers of intelligence.

The first layer is smart filtering. You can filter vendors by type — catering, venue, or AV. You can filter by event type — corporate, wedding, or party. You can set a budget with a real-time price slider from one thousand to eleven thousand dollars. And you can filter by star rating. All of these filters work together, live, as you adjust them.

The second layer is composite scoring. This is where the intelligence kicks in. We don't just show you a random list. We rank vendors using a weighted formula that accounts for price competitiveness, customer rating, and fit to your selected event type. If you're planning a wedding, wedding-specialized vendors float to the top. If you're on a tight budget, the most price-efficient options rank higher. The list adapts to you.

The third layer is rich vendor information. Click on any vendor and you get a full detail modal — contact name, email, phone number, a description of the vendor, their highlighted pros, their known limitations, guest capacity range, typical lead time, and their neighborhood. No more emailing vendors just to get basic information.

And then on top of all of this, we added two power features.

Vendor compare lets you select up to three vendors side-by-side, so you can make a direct decision without toggling between tabs. And the event date picker lets you set a date for your event, so you can think about availability context as you browse.

The platform is secured with session-based authentication — you log in once, and your session is maintained securely throughout your visit.

Now, the feature that really brings this platform to life is the AI assistant. I'll let Jaanvi walk you through what that looks like in action during our demo.

---
*[Transition: Rohini hands off to Jaanvi]*

---

---

## JAANVI — Live Demo Walkthrough
### Target time: 4 minutes (~520 words)

---

Thanks, Rohini. I'm Jaanvi, and I'm going to walk you through what it actually feels like to use Atelier.

*[Open browser to https://atelier.atelier-iq.workers.dev]*

The first thing you see is the login screen. Clean, minimal — consistent with the brand. We'll log in with our credentials.

*[Type username and password, click Log In]*

And here we are — the Atelier dashboard.

Right away, you can see the three sections of the interface: the filter panel on the left, the vendor grid in the center, and the AI chat panel on the right. The design is intentional — warm tones, editorial feel. This isn't meant to look like a standard SaaS tool. It's designed to feel like a premium service.

Let's say I'm planning a corporate dinner. I click "Corporate" in the event type filter.

*[Click Corporate pill]*

The vendor list immediately refreshes. Now let's say my budget is under six thousand dollars. I drag the price slider down.

*[Adjust slider]*

The list narrows. You can see the composite scores updating in real time — the vendors that are the best fit for a corporate event at this price point rise to the top.

Now let me click on one of the top-ranked caterers.

*[Click a catering vendor card]*

This is the vendor detail modal. You can see the contact name, email, and phone number — real information you can actually use. There's a description of the vendor, their pros, their limitations, their typical guest range, their lead time, and what neighborhood they're in. And at the bottom, three action buttons: Send Booking Inquiry, which opens a pre-filled professional email in your mail client. Book Now and Visit Website, which take you directly to Google search results for that vendor.

*[Show the buttons, click Send Booking Inquiry to show the pre-filled email draft]*

This saves real time. Instead of starting from scratch, the email is already drafted with the vendor's name, your context, and professional language.

Now let me show you the compare feature. I'll close this modal and select a few vendors.

*[Select 2–3 vendors using checkboxes or compare buttons]*

*[Open compare view]*

Side-by-side comparison — pricing, ratings, event types, capacity. Exactly what you'd want when you're narrowing down a shortlist.

And finally — the AI chat. This is where the course theme of generative AI really comes to life.

*[Click into the chat panel]*

I'll type: "Which venue has the highest rating for weddings under $8,000?"

*[Type and send the message, wait for response]*

And there it is — a real, grounded answer based on our dataset. The AI doesn't make up vendors. It doesn't hallucinate prices. It answers based on the 125 vendors we've curated. That's an intentional design choice, and Lynn is going to explain exactly why — and what's powering it under the hood.

Lynn, over to you.

---
*[Transition: Jaanvi hands off to Lynn]*

---

---

## LYNN — AI Component & Conclusion
### Target time: 4 minutes (~520 words)

---

Thank you, Jaanvi. I'm Lynn, and I want to talk about the part of this project that ties directly back to what this course is about — generative AI as a business tool.

Let's think about what just happened in that demo. Jaanvi typed a natural language question. The system understood it. It searched through our dataset. And it returned a specific, accurate, grounded answer in seconds. No manual search. No filter clicking. Just a question and an answer.

That's not magic. That's a well-designed AI integration. And I want to explain how we made it work — without getting too technical.

The AI assistant is powered by Anthropic's Claude model — specifically, claude-sonnet-4. We chose Claude because of its strong reasoning capabilities and its ability to stay grounded when given a specific knowledge base. One of the core challenges with large language models in business applications is hallucination — the model confidently making things up. In a vendor platform, that's a real problem. If the AI invents a vendor or fabricates a price, that's not just unhelpful, it breaks trust.

Our solution was to restrict the AI to our dataset. The model is given the full vendor catalog as context with every conversation. It cannot go outside that data. When you ask it a question about vendors, it answers from real information we've curated. When you ask something it can't answer from the dataset, it tells you that honestly. That design choice — keeping the AI grounded — was deliberate, and it reflects how we think AI should be used in serious business applications.

We also gave the AI a web search capability for general event planning questions — things like "what's the typical catering cost per person for a corporate dinner in New York?" — where pulling in current market context adds real value. But for vendor-specific queries, the model stays within our dataset.

From a technical standpoint, all AI calls are routed through our own secure backend. The API key never touches the browser. Users can optionally provide their own Anthropic key if they want to use their own account, and that's stored only in their browser's local storage — never transmitted to any third party.

Now — stepping back — I want to connect this to the bigger picture.

This course is called Developing Business Applications using GenAI. And I think what we've built here is a real example of what that means in practice. We didn't use AI as a gimmick. We didn't add a chatbot just to say we have one. We identified a genuine pain point — the friction in vendor discovery — and we used AI to meaningfully reduce that friction in a way that wouldn't have been possible five years ago.

Atelier is live. It's deployed. It's usable right now. And it reflects what we believe about the future of business tools — that AI isn't replacing human judgment, it's augmenting it. You still make the final call on which vendor to hire. Atelier just makes sure you're making that call with better information, faster.

Thank you for your time. We're happy to take any questions.

---
*[All four team members available for Q&A]*

---

---

## TIMING SUMMARY

| Speaker | Section | Target Time |
|---------|---------|-------------|
| Dhanvanth | Introduction & Problem Statement | 3.5 min |
| Rohini | Solution & Platform Features | 3.5 min |
| Jaanvi | Live Demo Walkthrough | 4.0 min |
| Lynn | AI Component & Conclusion | 4.0 min |
| **Total** | | **~15 min** |

---

## DEMO PREPARATION CHECKLIST

Before presenting:
- [ ] Log into https://atelier.atelier-iq.workers.dev and confirm it loads
- [ ] Have credentials ready: `Best Prof. Ever` / `Mr Nikouei`
- [ ] Pre-type (but don't send) the demo chat question so there's no typing delay
- [ ] Confirm your Anthropic API key is pasted into the chat panel (top of chat)
- [ ] Have the browser window at full screen, zoom set to ~90% so filters + grid + chat all fit
- [ ] Close all other browser tabs — clean screen for the demo
- [ ] Test the Send Booking Inquiry button beforehand so you know what the email draft looks like
