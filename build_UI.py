html = '''
<style>
  .flex-container {
  flex-direction: row-reverse;
    display: flex;
    flex-wrap: wrap;
	  line-height: 75px;
    justify-content: center;
    padding: 0;
    margin: 0;
  }
  .flex-item {
    display: flex;
    position: relative;
    margin-top: 10px;
    margin-right: 10px;
	width: 20%
  }
   a.button-tile {
    background: #e6f2ff;
    padding: 15px;
    width: 85vw;
    min-height: 97px;
    max-height: 250px;
    text-align: center;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px 0 hsla(0, 0%, 0%, 0.2);
  }
  a.button-tile:hover {
    background: #7aa9d391;
  } 
</style>
<div class="flex-container">
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/about/" class="button-tile">
            <h3 class="dark-title">About</h3>
            <p class="dark-text">Description and symptoms</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/communities/" class="button-tile">
            <h3 class="dark-title">Communities</h3>
            <p class="dark-text">Support groups for 21-Hydroxylase Deficiency</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/provider/" class="button-tile">
            <h3 class="dark-title">Providers</h3>
            <p class="dark-text">Healthcare providers in the area</p>
          </a>
        </div>

        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/research/" class="button-tile">
            <h3 class="dark-title">Research</h3>
            <p class="dark-text">Various sources of research on 21-Hydroxylase Deficiency</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/resources/" class="button-tile">
            <h3 class="dark-title">Financial Resources</h3>
            <p class="dark-text">Information about disability benefits from the Social Security Administration</p>
          </a>
        </div>
    </div>
'''
