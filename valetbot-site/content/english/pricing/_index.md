---
title: "Pricing"
subtitle: "Pricing should be simple. <hr> 
It's free if you have less than 5 spots. That's it ¯\\\\\_(ツ)_/¯ <br>"
# meta description
description: "This is meta description"
draft: false

basic:
  name : "Free plan"
  price: "$0"
  price_per : "month"
  info : "Try it out!"
  services:
  - "You get everything the bot can do."
  - "Up to 5 parking spots in 1 garage."
  button:
    enable : true
    label : "Get started for free"
    link : "/docs/installation"
    
business:
  name : "Paid Plan"
  price: "$5"
  price_per : "month"
  info : "Auto-manage your parking spots."
  services:
  - "You get everything the bot can do."
  - "Unlimited spots and garages."
  - " - "
  - "Coming soon!"
  button:
    enable : false
    label : "Proceed to payment"
    link : "/pricing"

call_to_action:
  enable : true
  title : "Need something special?"
  image : "images/payment.svg"
  content : "Need a custom integration? Want to add a command to the bot?"
  button:
    enable : true
    label : "Contact Us"
    link : "contact"
---