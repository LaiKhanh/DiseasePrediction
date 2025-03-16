<header>
	<!-- Left side of the header -->
	<nav>
		<a title="Home page" class="<?php echo ($page == 0 ? 'active' : ''); ?>" href="index.php">
			<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48">
				<path d="M39.5,43h-9c-1.381,0-2.5-1.119-2.5-2.5v-9c0-1.105-0.895-2-2-2h-4c-1.105,0-2,0.895-2,2v9c0,1.381-1.119,2.5-2.5,2.5h-9	C7.119,43,6,41.881,6,40.5V21.413c0-2.299,1.054-4.471,2.859-5.893L23.071,4.321c0.545-0.428,1.313-0.428,1.857,0L39.142,15.52	C40.947,16.942,42,19.113,42,21.411V40.5C42,41.881,40.881,43,39.5,43z"/>
			</svg>
		</a>
		<hr/>
		<a title="Friend list" class="<?php echo ($page == 1 ? 'active' : '') ; ?>" href="friendlist.php">
			<svg fill="#000000" width="800px" height="800px" viewBox="0 -64 640 640" xmlns="http://www.w3.org/2000/svg"><title>Friend list</title><path d="M192 256c61.9 0 112-50.1 112-112S253.9 32 192 32 80 82.1 80 144s50.1 112 112 112zm76.8 32h-8.3c-20.8 10-43.9 16-68.5 16s-47.6-6-68.5-16h-8.3C51.6 288 0 339.6 0 403.2V432c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48v-28.8c0-63.6-51.6-115.2-115.2-115.2zM480 256c53 0 96-43 96-96s-43-96-96-96-96 43-96 96 43 96 96 96zm48 32h-3.8c-13.9 4.8-28.6 8-44.2 8s-30.3-3.2-44.2-8H432c-20.4 0-39.2 5.9-55.7 15.4 24.4 26.3 39.7 61.2 39.7 99.8v38.4c0 2.2-.5 4.3-.6 6.4H592c26.5 0 48-21.5 48-48 0-61.9-50.1-112-112-112z"/></svg>
		</a>
		<hr/>
		<a title="Add new friend" class="<?php echo ($page == 2 ? 'active' : '') ; ?>" href="friendadd.php">
			<svg fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
				width="800px" height="800px" viewBox="0 0 45.402 45.402"
				xml:space="preserve"
			>
				<title>Add new friend</title>
				<g>
					<path d="M41.267,18.557H26.832V4.134C26.832,1.851,24.99,0,22.707,0c-2.283,0-4.124,1.851-4.124,4.135v14.432H4.141
						c-2.283,0-4.139,1.851-4.138,4.135c-0.001,1.141,0.46,2.187,1.207,2.934c0.748,0.749,1.78,1.222,2.92,1.222h14.453V41.27
						c0,1.142,0.453,2.176,1.201,2.922c0.748,0.748,1.777,1.211,2.919,1.211c2.282,0,4.129-1.851,4.129-4.133V26.857h14.435
						c2.283,0,4.134-1.867,4.133-4.15C45.399,20.425,43.548,18.557,41.267,18.557z"/>
				</g>
			</svg>
		</a>
		<hr/>
		<a title="About page" class="<?php echo ($page == 3 ? 'active' : '') ; ?>" href="about.php">
			<svg fill="none" viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
				<title>About</title>
				<g>
					<path d="M66,84H54V42a5.9966,5.9966,0,0,0-6-6H36a6,6,0,0,0,0,12h6V84H30a6,6,0,0,0,0,12H66a6,6,0,0,0,0-12Z"/>
					<path d="M48,24A12,12,0,1,0,36,12,12.0119,12.0119,0,0,0,48,24Z"/>
				</g>
			</svg>
		</a>
	</nav>
	<!-- Web name in the middle -->
	<h2>My Friends <br/>
		System
	</h2>
	<!-- Right side of the header -->
	<div class="user-actions">
		<?php
		if(
			isset($_SESSION["friend_id"]) && isset($_SESSION["friend_email"]) && isset($_SESSION["profile_name"])
		): ?> 
			<h3>Hello, <?php echo $_SESSION["profile_name"]?></h3>
			<a title="Sign up" class="signup <?php echo ($page == 4 ? 'active' : '') ; ?>" href="logout.php">
				<h4>Log out</h4>
			</a>
		<?php else: ?> 
			<a title="Sign in" class="signin <?php echo ($page == 4 ? 'active' : '') ; ?>" href="signin.php">
				<h4>Log in</h4>
			</a>
			<a title="Sign up" class="signup <?php echo ($page == 5 ? 'active' : '') ; ?>" href="signup.php">
				<h4>Sign up</h4>
			</a>
		<?php 
			endif;
		?>
	</div>
</header>