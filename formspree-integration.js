/* Sarah Safwan portfolio: Formspree submission handler */
(() => {
  'use strict';
  const endpoints = {'contact-form':'https://formspree.io/f/mdaqpozb','feedback-form':'https://formspree.io/f/mqpegrpn'};
  function initialize() {
    for (const [id, endpoint] of Object.entries(endpoints)) {
      const form=document.getElementById(id);
      if(!form || form.dataset.formspreeReady)continue;
      form.dataset.formspreeReady='true';
      form.addEventListener('submit', async event => {
        event.preventDefault(); event.stopImmediatePropagation();
        if(!form.reportValidity())return;
        const button=form.querySelector('[type="submit"]');
        const status=document.getElementById(id==='contact-form'?'form-status':'feedback-status') || (()=>{const el=document.createElement('p');el.setAttribute('role','status');el.setAttribute('aria-live','polite');form.append(el);return el})();
        const fields=new FormData(form);
        for (const input of form.querySelectorAll('input,select,textarea')) {
          if(input.disabled || ['submit','button','file'].includes(input.type))continue;
          const name=input.name || input.id;
          if(!name || (input.type==='checkbox' && !input.checked) || (input.type==='radio' && !input.checked))continue;
          if(!fields.has(name)) fields.append(name,input.value);
        }
        fields.set('_subject',id==='feedback-form'?'Portfolio feedback':'Sarah Safwan portfolio enquiry');
        fields.set('submission_source',location.pathname);
        if(id==='contact-form'){
          const params=new URLSearchParams(location.search);
          for(const key of ['from','service','package','market','custom']){if(params.has(key))fields.set('package_'+key,params.get(key));}
        }
        if(button)button.disabled=true;
        status.textContent='Sending your message…';
        try {
          const isProject=id==='contact-form'&&(new URLSearchParams(location.search).get('from')==='packages'||document.getElementById('enquiry-type')?.value==='project');
          const target=isProject?'https://formspree.io/f/xaeqlrea':endpoint;
          const response=await fetch(target,{method:'POST',body:fields,headers:{'Accept':'application/json'}});
          if(!response.ok){const data=await response.json().catch(()=>({}));throw new Error(data.errors?.map(x=>x.message).join(' ')||'Your message could not be sent. Please try again.');}
          status.textContent=id==='feedback-form'?'Thank you for sharing your feedback.':'Thank you for getting in touch. Your message has been sent.';
          form.reset();
        } catch (error) { status.textContent=error.message||'Submission failed. Please try again.'; }
        finally {if(button)button.disabled=false;}
      },true);
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
})();