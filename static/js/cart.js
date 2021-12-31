var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var flavor = this.dataset.flavor
		console.log('productId:', productId, 'Action:', action ,"flavor: " , flavor)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
			
		}else{
			updateUserOrder(productId , action, flavor )
		}
	})
}


function updateUserOrder(productId , action, flavor){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'flavor':flavor})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
//			location.reload()

		});
}



function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}
		

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	//location.reload()
}


//////////////////////////////////////////////
//wish list hart 
/////////////////////////////////////////////////


var updatemywishlist = document.getElementsByClassName('mywishlist')

for (i = 0; i < updatemywishlist.length; i++) {
	updatemywishlist[i].addEventListener('click', function(){
		var productId = this.dataset.product

		console.log('productId:', productId)

		if (user == 'AnonymousUser'){
      console.log('productId:', productId)

		}else{
			updatewishlist(productId )
		}
	})
}


    function updatewishlist(productId ){
	console.log('User is authenticated, sending data...')

		var url = '/updateWishList/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
//			location.reload()

		});
}
////////////////////////////////////////////////////////////