# Canvas page templates

Eight page templates that already satisfy the rules in `style-rules.md`. Use them
as the starting structure for a new page rather than inventing layout.

**Do not restyle a template.** The nesting, heading order, and callout structure are
what make it compliant. Fill in the placeholders and delete the sections you do not
need — that is all.

## Brand colors

Every template carries two placeholders. Substitute your institution's values before
use; they are the only branding the templates hold.

| Placeholder | Role | Accessibility obligation |
|---|---|---|
| `{{Color_1}}` | Primary. Background behind white text in H2 banners and callout bars; also the H3/H4 text color. | **Sits behind white text — must clear 4.5:1 against `#FFFFFF`.** A mid-tone brand color that looks right in a logo often fails here. |
| `{{Color_2}}` | Secondary. Rules and left borders only, never behind text. | None — it never carries text. |

Check `{{Color_1}}` before you use it:

```bash
printf '<div style="background:%s"><p style="color:#ffffff">test</p></div>' "#0369a1" \
  | python3 scripts/contrast.py -
```

## Placeholder conventions

- `[SQUARE BRACKETS]` — replace with real content, or delete the section.
- `{{curly braces}}` — replace with real content.
- Bracketed *instructions* (e.g. `[Insert banner with dimensions 1200x400 pixels...]`)
  describe what to put there; they are not content to paste.

Never invent course descriptions or Student Learning Outcomes to fill a placeholder.
Leave the placeholder in place and say what is still needed — see `style-rules.md`.

## A note on these templates

These were transcribed from the source guides, which carried two HTML defects that
would break rendering in Canvas. Both are corrected here:

- 27 callout `<div>`s had an unterminated `style` attribute
  (`border-radius: 5px;>` with no closing quote).
- 2 `<h4>` elements in Template 4 were closed with `</h3>`.


## Template 1 — General Content Page

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>[Title]</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">  
   
     <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Heading 3</strong></h3>  
<div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <p>{{add content}}</p>  
    <h4><span style="color: {{Color_1}};"><strong>Heading 4</strong></span></h4>  
    <p>{{add content}}</p>  
    </div>

    <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Heading 3</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>{{add content}}</p>  
        <h4><span style="color: {{Color_1}};"><strong>Heading 4</strong></span></h4>  
        <p>{{add content}}</p>  
    </div>

</div>

<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
    <p style="text-align: right;"><em>Click on the Next button below to continue.</em> <span aria-hidden="true">▼</span></p>  
</div>

    </div>  
</div>
```

## Template 2 — Front Page

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>[Course Number and Title]</strong></h2>

[Insert banner with dimensions 1200x400 pixels based on the course name. Center image.]

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">  

    <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Class Information</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <p><strong>Location:</strong> [LOCATION]<strong>Meeting Days and Time:</strong> [CLASS DAYS and TIMES]<strong>Instructor:</strong> [INSTRUCTOR NAME]<strong>In-Person Office Hours:</strong> [IN-PERSON OFFICE HOUR DAY AND TIME]<strong>Office Location:</strong> [OFFICE LOCATION]  
<strong>Online Office Hours:</strong> [ONLINE OFFICE HOUR DAY AND TIME]<strong>Zoom Link:</strong> [ZOOM LINK]</p>  
[IF link provided, embed welcome video from instructor.]  
</div>

         <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Course Overview</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>Welcome to [Course Name]!</p>  
        <p>[Insert course description.]</p>  
        </div>

   <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Student Learning Outcomes</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <ol style="list-style-type: decimal;">  
            <li>[SLO 1].</li>  
            <li>[SLO 2].</li>  
            <li>[SLO 3].</li>  
        </ol>  
    </div>  
</div>

<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
  <h3 style="text-align: center;"><strong>Course Navigation</strong></h3>  
        <p style="text-align: center;"><span>To access course information and resources, select <strong>Modules</strong> on the left-hand menu.</span></p>  
</div>  
    </div>  
</div>
```

## Template 3 — Canvas Announcement

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>[Title]</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">  
 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Heading 3</strong></h3>  
<div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <p>{{add content}}</p>  
    </div>

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Heading 3</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>{{add content}}</p>  
    </div>

</div>  
   </div>  
</div>
```

## Template 4 — Meet Your Instructor Page

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>Hello, my name is [Instructor Name]!</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">  
 [Image of instructor. Center the image. If image not provided, do not generate an image.]   

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Quick Introduction</strong></h3>

 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
<p>[A short description about the instructor.]</p>  
</div>

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>3 Fun Facts About Me</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <ol>  
        <li>[Fun fact 1]</li>  
        <li>[Fun fact 2]</li>  
        <li>[Fun fact 3]</li>  
    </ol>  
</div>

<h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Hours</strong></h3>   
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
<p><strong>In-Person Office Hours:</strong> [IN-PERSON OFFICE HOUR DAY AND TIME]<strong>Office Location:</strong> [OFFICE LOCATION]  
<strong>Online Office Hours:</strong> [ONLINE OFFICE HOUR DAY AND TIME]<strong>Zoom Link:</strong> [ZOOM LINK]</p>

</div>

  <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Contact Information</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
     
    <h4><strong><span style="color: {{Color_1}};">The best way to contact me:</span></strong></h4>  
<p>[Insert preferred method of contact: institutional email address OR Canvas Inbox feature. IF Canvas Inbox, include hyperlink: https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-use-the-Inbox/ta-p/616671]</p>  
    <h4><strong><span style="color: {{Color_1}};">Response Time</span></strong></h4>  
<p>I will respond to you within [Insert time window for responses to students.]</p>  
</div>

</div>

<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
    <p style="text-align: right;"><em>Click on the Next button below to continue.</em> <span aria-hidden="true">▼</span></p>  
</div>  
    </div>  
</div>
```

## Template 5 — Module Overview Page

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>[NAME OF TOPIC]</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Overview</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <p>[Overview of the information being covered this week.]</p>  
</div>  
     
        <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Objective</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>By the end of this week, you will be able to:</p>  
        <ul>  
            <li>[Objective 1]</li>  
            <li>[Objective 2]</li>  
        </ul>  
    </div>

       <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Agenda for the Week</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <h4><strong><span style="color: {{Color_1}};">Read:</span></strong></h4>  
        <ul>  
            <li>[Reading title]</li>  
            <li>[Reading title]</li>  
        </ul>  
        <h4><strong><span style="color: {{Color_1}};">Watch:</span></strong></h4>  
        <ul>  
            <li>[Video title]</li>  
            <li>[Video title]</li>  
        </ul>  
        <h4><strong><span style="color: {{Color_1}};">Complete the following assignments:</span></strong></h4>  
        <ul>  
            <li>[Assignment or quiz title]</li>  
            <li>[Assignment or quiz title]</li>  
        </ul>  
    </div>

</div>

<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
    <p style="text-align: right;"><em>Click on the Next button below to continue.</em> <span aria-hidden="true">▼</span></p>  
</div>  
    </div>  
</div>
```

## Template 6 — Assignment Instructions

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>Assignment Title</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">

   <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Assignment Description and Instructions</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
    <p>[Assignment description: describes what the assignment is and explains the purpose of the assignment.]</p>  
 <p>[Assignment instructions e.g. “Write a paper in response to the following prompt…”]</p>  
    </div>

           <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Technical Requirements</strong></h3>  
     <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <ul>  
<li><strong>Due Date:</strong> [DUE DATE]</li>  
            <li><strong>Page Length/Word Count Requirement:</strong> [PAGE LENGTH OR WORD COUNT REQUIREMENT]</li>  
             <li><strong>Formatting Requirement:</strong> [FORMATTING REQUIREMENT e.g. MLA or APA]</li>  
        </ul>  
    </div>

    <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Grading</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>[Description of how the assignment will be graded and how it will be weighted in the student's final grade. If rubric is used, state: “View the assignment rubric for more details.”]</p>  
</div>  
         
            <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Canvas Support</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
            <ul>  
                <li><a href="https://guides.instructure.com/m/4212/l/54352-how-do-i-view-the-rubric-for-my-assignment">How do I view the rubric for my assignment?</a></li>  
                <li><a href="https://guides.instructure.com/m/4212/l/41972-how-do-i-submit-an-online-assignment">How do I submit an online assignment?</a></li>  
                <li><a href="https://guides.instructure.com/m/4212/l/54358-how-do-i-know-when-my-instructor-has-graded-my-assignment">How do I know when my instructor has graded my assignment?</a></li>  
            </ul>  
        </div>

           <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Directions to Submit</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
            <ol>  
                <li>On the right hand Menu, you will see a <strong>START ASSIGNMENT</strong> button with a white plus sign.</li>  
                <li>Click on the <strong>SUBMIT ASSIGNMENT</strong> button. Then click <strong>Choose a file to upload</strong> to look for your file on your computer.</li>  
                <li>When done, click the <strong>SUBMIT ASSIGNMENT</strong> button.</li>  
            </ol>  
        </div>  
</div>

<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
    <p style="text-align: right;"><em>Click on the Next button below to continue.</em> <span aria-hidden="true">▼</span></p>  
</div>  
    </div>  
</div>
```

## Template 7 — Discussion Board

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>[Title of discussion]</strong></h2>

<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">

     <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Topic Overview</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">    <p>[Discussion topic summary.]</p>  
    </div>

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Discussion Questions</strong></h3>  
   <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  <ol>  
        <li>[Discussion question 1]</li>  
        <li>[Discussion question 2]</li>  
        <li>[Discussion question 3]</li>  
    </ol>  
</div>

       <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Technical Support</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">     
     <p>Need help using Canvas Discussions? If so, please review the following Canvas guide pages:</p>  
        <ul>  
            <li><a href="https://community.canvaslms.com/docs/DOC-10561-4212190706" target="_blank" rel="noopener">How to reply to a discussion as a student</a></li>  
            <li><a href="https://community.canvaslms.com/docs/DOC-10701-canvas-student-guide-table-of-contents#jive_content_id_Discussions" target="_blank" rel="noopener">Canvas Student Guide for Discussions</a></li>  
            <li><a href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-upload-a-video-using-the-Rich-Content-Editor-as-a/ta-p/429" target="_blank" rel="noopener">How to upload a video to a discussion</a></li>  
            <li><a href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-embed-an-image-in-a-discussion-reply-as-a-student/ta-p/313" target="_blank" rel="noopener">How to embed an image in a discussion</a></li>  
        </ul>  
</div>

  <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Submission Instructions and Due Dates</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>Click "<em>Reply</em>" to post your question.</p>  
        <p><strong>First response due:</strong> <em>[Due Date 1, Time 1]</em></p>  
        <p><strong>Responses to peers due:</strong> <em>[Due Date 2, Time 2]</em></p>

</div>  
</div>  
<div style="background-color: {{Color_1}}; color: white; padding: 5px; margin-top: 5px; border-radius: 5px; text-align: center;">  
    <p style="text-align: right;"><em>Click on the Next button below to continue.</em> <span aria-hidden="true">▼</span></p>  
</div>  
    </div>  
</div>
```

## Template 8 — Quiz Template

```html
<div style="padding: 20px; border-radius: 5px;">  
    <div style="padding: 20px; border-radius: 5px;">

<h2 class="content-box pad-box-large" style="background-color: {{Color_1}}; color: white; border-radius: 5px; padding: 16px;"><strong>Quiz Overview</strong></h2>  
<div class="border border-b" style="border-color: #FFFFFF; padding-left: 15px; padding-right: 15px;">

    <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Goal and Purpose</strong></h3>  
  <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">   <p>{{Insert goal and purpose of the quiz here.}}</p>  
</div>

 <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Directions</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <ul>  
            <li>You have {{number}} attempts to take the quiz.</li>  
            <li>This quiz is {{timed/untimed}}.</li>  
        </ul>  
    </div>  
    
  <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Grading</strong></h3>  
       <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  <p>If for any reason you feel that your score is wrong, please send me a message through the Canvas INBOX.</p>  
    </div>

      <h3 style="color: {{Color_1}}; border-bottom: 2px solid {{Color_2}}; padding-bottom: 5px;"><strong>Technical Support</strong></h3>  
 <div style="border-left: 5px solid {{Color_2}}; padding: 20px; margin-bottom: 25px; border-radius: 5px;">  
        <p>Need help using Canvas Quizzes? If so, please review the following Canvas resources:</p>  
        <ul>  
            <li><span><a class="jive-link-wiki-small external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-take-a-quiz-in-New-Quizzes/ta-p/291" target="_blank" rel="noopener" data-containerid="2558" data-containertype="14" data-objectid="10645" data-objecttype="102">How do I take a quiz in New Quizzes?</a></span></li>  
            <li><span><a class="jive-link-wiki-small external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-take-a-quiz-where-I-can-only-view-one-question-at-a/ta-p/292" target="_blank" rel="noopener" data-containerid="2558" data-containertype="14" data-objectid="10582" data-objecttype="102">How do I take a quiz where I can only view one question at a time in New Quizzes?</a></span></li>  
            <li><span><a class="jive-link-wiki-small external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-answer-each-type-of-question-in-New-Quizzes/ta-p/290" target="_blank" rel="noopener" data-containerid="2558" data-containertype="14" data-objectid="10583" data-objecttype="102">How do I answer each type of question in New Quizzes?</a></span></li>  
            <li><span><a class="jive-link-wiki-small external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-submit-a-quiz/ta-p/475" target="_blank" rel="noopener" data-containerid="2558" data-containertype="14" data-objectid="10685" data-objecttype="102">How do I submit a quiz?</a></span></li>  
            <li><span><a class="jive-link-wiki-small external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-view-my-quiz-results-as-a-student-in-New-Quizzes/ta-p/289" target="_blank" rel="noopener" data-containerid="2558" data-containertype="14" data-objectid="10572" data-objecttype="102">How do I view my quiz results as a student in New Quizzes?</a></span></li>  
            <li><a class="external" href="https://community.canvaslms.com/t5/Student-Guide/How-do-I-know-if-I-can-retake-a-quiz-in-New-Quizzes/ta-p/287" target="_blank" rel="noopener">How do I know if I can retake a quiz in New Quizzes?</a></li>  
        </ul>  
    </div>  
</div>  
    </div>  
</div>
```
